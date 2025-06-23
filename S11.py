import os
import subprocess
import shutil
import zipfile
import sys
import ssl
import requests
from colorama import init, Fore
from tqdm import tqdm
import concurrent.futures

init(autoreset=True)

EMOJI = {
    "menu": "🧩",
    "done": "✅",
    "error": "❌",
    "clear": "🧹",
    "download": "⬇️",
    "extract": "📂",
    "exit": "👋",
    "gear": "⚙️",
    "id": "🪪"
}

REPO_URL = "https://codeload.github.com/ENMN11/NexusHideout/zip/refs/heads/main"
HOME_DIR = "/data/data/com.termux/files/home"
ZIP_PATH = os.path.join(HOME_DIR, "Nexus.zip")
EXTRACTED_DIR = os.path.join(HOME_DIR, "Nexus")
DOWNLOADS_DIR = "/storage/emulated/0/Download"
AUTOEXEC_DIR = "/storage/emulated/0/Codex/Autoexec"
ANDROID_ID = "9c47a1f3b6e8d2c5"

APKS = {
    "MTManager.apk": "bin.mt.plus",
    "XBrowser.apk": "com.xbrowser.play",
    "PocoLauncher.apk": "com.mi.android.globallaunches"
}

EXTRA_FILES = ["config-change.json", "Rejoin.py", "Cookie.txt"]
AUTOEXEC_FILES = ["BananaHubGOD.txt", "Trackstat.txt"]

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def run_command(cmd, suppress_output=True, check_success=False):
    stdout_redir = subprocess.DEVNULL if suppress_output else None
    stderr_redir = subprocess.DEVNULL if suppress_output else None
    try:
        result = subprocess.run(cmd, stdout=stdout_redir, stderr=stderr_redir, text=True, check=check_success)
        return result
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(Fore.LIGHTRED_EX + f"Error Running Command '{' '.join(cmd)}': {e}")
        return None
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Unknown Error Running Command '{' '.join(cmd)}': {e}")
        return None

def check_root_permissions():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error Checking Root Permissions: {e}")
        return False

def is_package_installed(pkg_name):
    package_dir = os.path.join("/data/data", pkg_name)
    return os.path.isdir(package_dir)

def disable_play_store():
    print(Fore.LIGHTYELLOW_EX + "Disabling Google Play Store...", end=" ")
    if run_command(["pm", "disable-user", "--user", "0", "com.android.vending"], check_success=True):
        print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Completed")
    else:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Failed (May Already Be Disabled Or No Permission)")

def disable_old_launcher():
    print(Fore.LIGHTYELLOW_EX + "Disabling Old Launcher...", end=" ")
    if run_command(["pm", "disable-user", "--user", "0", "com.og.launcher"], check_success=True):
        print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Completed")
    else:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Failed (May Already Be Disabled Or No Permission)")

def set_android_id():
    print(Fore.LIGHTYELLOW_EX + f"Setting Android Id To {ANDROID_ID}...", end=" ")
    if run_command(["settings", "put", "secure", "android_id", ANDROID_ID], check_success=True):
        print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Completed")
    else:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Failed (May No Permission)")

def set_default_launcher(pkg_name):
    print(Fore.LIGHTYELLOW_EX + f"Setting {pkg_name} as Default Launcher...", end=" ")
    try:
        # Clear any existing default launcher
        run_command(["pm", "clear-preferred-activities", "--user", "0"], check_success=True)
        
        # Set the package as the default launcher for the HOME intent
        launcher_cmd = [
            "am", "set-preferred-activity",
            "--user", "0",
            "-a", "android.intent.action.MAIN",
            "-c", "android.intent.category.HOME",
            "-c", "android.intent.category.DEFAULT",
            "-n", f"{pkg_name}/.MainActivity"
        ]
        if run_command(launcher_cmd, check_success=True):
            print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Completed")
            return True
        else:
            print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Failed to Set Default Launcher")
            return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Error Setting Default Launcher: {e}")
        return False

def install_apk(apk_file, pkg_name):
    apk_path = os.path.join(EXTRACTED_DIR, apk_file)
    print(Fore.LIGHTYELLOW_EX + f"Installing {apk_file}...", end=" ")

    if is_package_installed(pkg_name):
        print(Fore.LIGHTCYAN_EX + f"{EMOJI['done']} {pkg_name} Already Installed")
        # If it's the launcher, ensure it's set as default
        if pkg_name == "com.mi.android.globallaunches":
            set_default_launcher(pkg_name)
        return True

    if not os.path.exists(apk_path):
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Apk File Not Found: {apk_path}")
        return False

    try:
        install_cmd = ["pm", "install", "-r", "--full", apk_path]
        if run_command(install_cmd, check_success=True):
            print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Installed {apk_file} Successfully")
            # If it's the launcher, set it as default
            if pkg_name == "com.mi.android.globallaunches":
                set_default_launcher(pkg_name)
            return True
        else:
            print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Installation Failed For {apk_file}")
            return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Error Installing {apk_file}: {e}")
        return False

def allow_unknown_sources(pkg_name):
    print(Fore.LIGHTYELLOW_EX + f"Enabling Unknown Sources For {pkg_name}...", end=" ")
    # Use settings to enable REQUEST_INSTALL_PACKAGES without appops
    if run_command(["settings", "put", "secure", "install_non_market_apps", "1"], check_success=True):
        print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Completed")
    else:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Failed (May No Permission)")

def move_extracted_files(files_to_move, destination_directory):
    print(Fore.LIGHTYELLOW_EX + f"Moving Files To {destination_directory}...")
    try:
        if destination_directory == AUTOEXEC_DIR:
            if os.path.exists(AUTOEXEC_DIR):
                print(Fore.LIGHTCYAN_EX + f"Deleting Old Directory: {AUTOEXEC_DIR}")
                shutil.rmtree(AUTOEXEC_DIR)
            os.makedirs(AUTOEXEC_DIR)
        else:
            os.makedirs(destination_directory, exist_ok=True)
    except OSError as e:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Error Creating Or Deleting Destination Directory {destination_directory}: {e}")
        return

    for file_name in files_to_move:
        source_path = os.path.join(EXTRACTED_DIR, file_name)
        destination_path = os.path.join(destination_directory, file_name)
        if not os.path.exists(source_path):
            print(Fore.LIGHTRED_EX + f"  {EMOJI['error']} Source File Not Found: {source_path}, Skipping")
            continue
        try:
            if os.path.exists(destination_path):
                os.remove(destination_path)
            shutil.move(source_path, destination_path)
            print(Fore.LIGHTGREEN_EX + f"  {EMOJI['done']} Moved: {file_name}")
        except (shutil.Error, Exception) as e:
            print(Fore.LIGHTRED_EX + f"  {EMOJI['error']} Error Moving {file_name}: {e}")

_session = None

def get_requests_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})
    return _session

def download_file_with_progress(url, destination):
    print(Fore.LIGHTBLUE_EX + f"{EMOJI['download']} Downloading From {url}...")
    session = get_requests_session()
    
    try:
        block_size = 100000
        response = session.get(url, stream=True, verify=False, timeout=60)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        
        with tqdm(total=total_size, unit='iB', unit_scale=True, desc=os.path.basename(destination), ncols=100) as pbar:
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Downloaded {os.path.basename(destination)} Successfully")
        return True
    except requests.exceptions.Timeout:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Timeout Error Downloading {url}. Connection Too Slow Or Blocked")
        if os.path.exists(destination):
            os.remove(destination)
        return False
    except requests.exceptions.RequestException as e:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Error Downloading {url}: {e}")
        if os.path.exists(destination):
            os.remove(destination)
        return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Unknown Error Downloading {url}: {e}")
        if os.path.exists(destination):
            os.remove(destination)
        return False

def extract_zip_file(zip_path, extract_to_dir):
    print(Fore.LIGHTBLUE_EX + f"{EMOJI['extract']} Extracting {os.path.basename(zip_path)} To {extract_to_dir}...")

    if os.path.exists(extract_to_dir):
        try:
            print(Fore.LIGHTYELLOW_EX + f"  {EMOJI['clear']} Deleting Old Directory: {extract_to_dir}")
            shutil.rmtree(extract_to_dir)
        except OSError as e:
            print(Fore.LIGHTRED_EX + f"  {EMOJI['error']} Error Deleting Old Directory {extract_to_dir}: {e}")
            return False
    
    try:
        os.makedirs(extract_to_dir)
    except OSError as e:
        print(Fore.LIGHTRED_EX + f"  {EMOJI['error']} Error Creating Destination Directory {extract_to_dir}: {e}")
        return False

    temp_extract_dir = os.path.join(os.path.dirname(zip_path), "temp_zip_extract")
    if os.path.exists(temp_extract_dir):
        shutil.rmtree(temp_extract_dir)
    os.makedirs(temp_extract_dir)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)

            extracted_items = os.listdir(temp_extract_dir)
            
            if len(extracted_items) == 1 and os.path.isdir(os.path.join(temp_extract_dir, extracted_items[0])):
                source_path = os.path.join(temp_extract_dir, extracted_items[0])
                print(Fore.LIGHTYELLOW_EX + f"  {EMOJI['gear']} Detected Root Directory '{extracted_items[0]}', Moving Contents...")
                for item in os.listdir(source_path):
                    shutil.move(os.path.join(source_path, item), extract_to_dir)
            else:
                print(Fore.LIGHTYELLOW_EX + f"  {EMOJI['gear']} Moving Files Directly From Temporary Directory...")
                for item in os.listdir(temp_extract_dir):
                    shutil.move(os.path.join(temp_extract_dir, item), extract_to_dir)

        print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Extraction Successful")
        return True
    except zipfile.BadZipFile:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Corrupted Zip File: {zip_path}")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Error Extracting {zip_path}: {e}")
        return False
    finally:
        if os.path.exists(temp_extract_dir):
            try:
                shutil.rmtree(temp_extract_dir)
                print(Fore.LIGHTCYAN_EX + f"  {EMOJI['clear']} Cleaned Up Temporary Directory")
            except OSError as e:
                print(Fore.LIGHTRED_EX + f"  {EMOJI['error']} Error Cleaning Up Temporary Directory {temp_extract_dir}: {e}")

def download_and_prepare_repository(update=False):
    clear_screen()
    
    if update and os.path.exists(ZIP_PATH):
        print(Fore.LIGHTYELLOW_EX + f"Deleting Old Zip File: {ZIP_PATH}...")
        try:
            os.remove(ZIP_PATH)
            print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Deleted Old Zip File")
        except OSError as e:
            print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Error Deleting Old Zip File: {e}")
            return False
            
    if not os.path.exists(ZIP_PATH):
        if not download_file_with_progress(REPO_URL, ZIP_PATH):
            return False

    if not extract_zip_file(ZIP_PATH, EXTRACTED_DIR):
        return False
    
    return True

def perform_setup():
    clear_screen()
    print(Fore.LIGHTBLUE_EX + f"{EMOJI['gear']} Starting Setup Process...")

    if not check_root_permissions():
        print(Fore.LIGHTRED_EX + f"{EMOJI['error']} Root Permissions Required. Please Grant Root Permissions To Termux And Try Again")
        return False
    else:
        print(Fore.LIGHTGREEN_EX + f"{EMOJI['done']} Root Permissions Granted")
    
    disable_play_store()
    disable_old_launcher()
    set_android_id()
    
    move_extracted_files(EXTRA_FILES, DOWNLOADS_DIR)
    move_extracted_files(AUTOEXEC_FILES, AUTOEXEC_DIR)
    
    all_apks_installed = True
    for apk_file, pkg_name in APKS.items():
        if not install_apk(apk_file, pkg_name):
            all_apks_installed = False
        else:
            allow_unknown_sources(pkg_name)
    
    return all_apks_installed

def main_menu():
    while True:
        clear_screen()
        print(Fore.LIGHTWHITE_EX + r"""
  _______           /\          ________         _________ .__  .__        __ 
  \       \ ____ ___  _____ __ _____)/______ \_____  \____  ____  \_  ___ \|  | |__| ____ |  | __
  /  _  _ \_/ __ \\ \/  /  |  \/  ___//  ___/  /  _  _ \/  _  _ \_/ __ \  /    \  \/|  | |  |/ ___\|  |/ /
 /  /_\  \ \  ___/ >  <|  |  /\___ \ \___ \  /  /_\  \ \  \_/  \  ___/  \    ___|  |_|  \  \___|  < 
 \_______  /\___  >__/\_ \____//____  >____  > \_______  /\____/\___  >  \______  /____/__|\___  >__|_ \
         \/     \/      \/          \/     \/          \/          \/          \/          \/     \/   \/
        """)
        print(Fore.LIGHTBLUE_EX + "[1] Setup (Initial Installation)")
        print(Fore.LIGHTMAGENTA_EX + "[2] Update (Download And Reinstall)")
        print(Fore.LIGHTRED_EX + "[3] Exit")
        
        choice = input(Fore.LIGHTWHITE_EX + f"{EMOJI['menu']} Please Select Your Setup Option: ")
        
        if choice == "1":
            print(Fore.LIGHTBLUE_EX + f"\n{EMOJI['gear']} Starting Installation...")
            if download_and_prepare_repository(update=False):
                if perform_setup():
                    print(Fore.LIGHTGREEN_EX + f"\n{EMOJI['done']} Installation Completed Successfully")
                else:
                    print(Fore.LIGHTRED_EX + f"\n{EMOJI['error']} Installation Failed. Please Check Errors Above")
            else:
                print(Fore.LIGHTRED_EX + f"\n{EMOJI['error']} Download Or Repository Preparation Failed")
            input(Fore.LIGHTWHITE_EX + "Press Enter To Return To Main Menu...")
        elif choice == "2":
            print(Fore.LIGHTBLUE_EX + f"\n{EMOJI['gear']} Starting Update...")
            if download_and_prepare_repository(update=True):
                if perform_setup():
                    print(Fore.LIGHTGREEN_EX + f"\n{EMOJI['done']} Update Completed Successfully")
                else:
                    print(Fore.LIGHTRED_EX + f"\n{EMOJI['error']} Update Failed. Please Check Errors Above")
            else:
                print(Fore.LIGHTRED_EX + f"\n{EMOJI['error']} Download Or Repository Preparation For Update Failed")
            input(Fore.LIGHTWHITE_EX + "Press Enter To Return To Main Menu...")
        elif choice == "3":
            print(Fore.LIGHTRED_EX + f"{EMOJI['exit']} Exiting...")
            sys.exit(0)
        else:
            input(Fore.LIGHTWHITE_EX + "Invalid Choice, Press Enter To Try Again...")

if __name__ == "__main__":
    main_menu()
