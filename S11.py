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

REPO_URL = "https://codeload.github.com/ENMN11/NexusHideout/zip/refs/heads/main"
HOME_DIR = "/data/data/com.termux/files/home"
ZIP_PATH = os.path.join(HOME_DIR, "Nexus.zip")
EXTRACTED_DIR = os.path.join(HOME_DIR, "Nexus")
DOWNLOADS_DIR = "/storage/emulated/0/Download"
AUTOEXEC_DIR = "/storage/emulated/0/RonixExploit/autoexec"
ANDROID_ID = "36ea1127de363534"

APKS = {
    "MTManager.apk": "bin.mt.plus",
    "XBrowser.apk": "com.xbrowser.play",
    "PocoLauncher.apk": "com.mi.android.globallaunches"
}

EXTRA_FILES = ["config-change.json", "Rejoin.py", "Cookie.txt", "FPS.py"]
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

def disable_bloatware_apps():
    apps_to_disable = [
        "com.google.android.googlequicksearchbox",
        "com.google.android.gms",
        "com.android.chrome",
        "com.google.android.gm",
        "com.google.android.youtube",
        "com.google.android.apps.docs",
        "com.google.android.apps.meetings",
        "com.google.android.apps.maps",
        "com.google.android.apps.photos",
        "com.google.android.contacts",
        "com.google.android.calendar",
        "com.android.vending",
        "com.google.ar.core",
        "com.google.android.play.games",
        "com.google.android.apps.magazines",
        "com.google.android.apps.subscriptions.red",
        "com.google.android.videos",
        "com.google.android.apps.googleassistant",
        "com.google.android.apps.messaging",
        "com.google.android.dialer",
        "com.android.mms",
        "com.android.dialer",
        "com.android.contacts",
        "com.android.calendar",
        "com.google.android.apps.gallery",
        "com.google.android.apps.wellbeing",
        "com.google.android.apps.googleone",
        "com.google.android.apps.nbu.files",
        "com.og.launcher",
        "com.sec.android.gallery3d",
        "com.miui.gallery",
        "com.coloros.gallery3d",
        "com.vivo.gallery",
        "com.motorola.gallery",
        "com.transsion.gallery",
        "com.sonyericsson.album",
        "com.lge.gallery",
        "com.htc.album",
        "com.huawei.photos",
        "com.android.gallery3d",
        "com.android.gallery",
        "com.google.android.deskclock",
        "com.sec.android.app.clockpackage",
        "com.miui.clock",
        "com.coloros.alarmclock",
        "com.vivo.alarmclock",
        "com.motorola.timeweatherwidget",
        "com.android.deskclock",
        "com.huawei.clock",
        "com.lge.clock",
        "com.android.email",
        "com.android.printspooler",
        "com.android.bookmarkprovider",
        "com.android.bips",
        "com.android.cellbroadcastreceiver",
        "com.android.cellbroadcastservice",
        "com.android.dreams.basic",
        "com.android.dreams.phototable",
        "com.android.wallpaperbackup",
        "com.android.wallpapercropper",
        "com.android.statementservice",
        "com.android.hotwordenrollment.okgoogle",
        "com.android.hotwordenrollment.xgoogle",
        "com.android.sharedstoragebackup",
        "com.android.vpndialogs",
        "com.android.stk",
        "com.android.traceur",
        "com.google.android.feedback",
        "com.google.android.tts",
        "com.google.android.projection.gearhead",
        "com.google.android.inputmethod.latin",
        "com.google.android.setupwizard",
        "com.google.android.marvin.talkback",
        "com.google.android.apps.tips",
        "com.google.android.location.history",
        "com.google.android.printservice.recommendation",
        "com.google.ar.lens",
        "com.google.android.as",
        "com.google.android.configupdater",
        "com.google.android.backuptransport",
        "com.google.android.syncadapters.contacts",
        "com.google.android.syncadapters.calendar",
        "com.google.android.gsf",
        "com.google.android.gsf.login",
        "com.qualcomm.qti.qms.service.telemetry",
        "com.qualcomm.qti.qms.service.connectionsecurity",
        "com.qualcomm.qti.qms.service.trustzoneaccess",
        "com.qualcomm.qti.uim",
        "com.qualcomm.qti.devicestatisticsservice",
        "com.android.se",
        "com.android.nfc",
        "com.android.simappdialog",
        "com.google.android.tag",
        "com.android.bluetoothmidiservice",
        "com.google.android.apps.messaging",
        "com.google.android.dialer",
        "com.android.mms",
        "com.android.messaging",
        "com.android.dialer",
        "com.android.contacts",
        "com.samsung.android.messaging",
        "com.android.mms.service",
        "com.miui.smsservice",
        "com.coloros.mms",
        "com.vivo.message",
        "com.huawei.message",
        "com.lge.message",
        "com.sonyericsson.conversations",
        "com.motorola.messaging",
        "com.transsion.message",
        "com.android.cellbroadcastreceiver",
        "com.android.cellbroadcastservice"
    ]

    for package_name in apps_to_disable:
        if run_command(["pm", "disable-user", "--user", "0", package_name], check_success=True):
            print(Fore.LIGHTGREEN_EX + f"Disabled {package_name}")

def set_android_id():
    print(Fore.LIGHTYELLOW_EX + f"Setting Android ID to {ANDROID_ID}...", end=" ")
    if run_command(["settings", "put", "secure", "android_id", ANDROID_ID], check_success=True):
        print(Fore.LIGHTGREEN_EX + "Completed")
        return True
    else:
        print(Fore.LIGHTRED_EX + "Failed to Set Android ID")
        return False

def install_apk(apk_file, pkg_name):
    apk_path = os.path.join(EXTRACTED_DIR, apk_file)
    print(Fore.LIGHTYELLOW_EX + f"Installing {apk_file}...", end=" ")

    if is_package_installed(pkg_name):
        print(Fore.LIGHTCYAN_EX + f"{pkg_name} Already Installed")
        return True

    if not os.path.exists(apk_path):
        print(Fore.LIGHTRED_EX + f"APK File Not Found: {apk_path}")
        return False

    try:
        install_cmd = ["pm", "install", "-r", "--full", apk_path]
        result = run_command(install_cmd, check_success=False)
        
        if result and result.returncode == 0:
            print(Fore.LIGHTGREEN_EX + f"Installed {apk_file} Successfully")
            return True
        else:
            print(Fore.LIGHTRED_EX + f"Installation Failed For {apk_file}")
            return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error Installing {apk_file}: {e}")
        return False

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
        print(Fore.LIGHTRED_EX + f"Error Creating Or Deleting Destination Directory {destination_directory}: {e}")
        return

    for file_name in files_to_move:
        source_path = os.path.join(EXTRACTED_DIR, file_name)
        destination_path = os.path.join(destination_directory, file_name)
        if not os.path.exists(source_path):
            print(Fore.LIGHTRED_EX + f"Source File Not Found: {source_path}, Skipping")
            continue
        try:
            if os.path.exists(destination_path):
                os.remove(destination_path)
            shutil.move(source_path, destination_path)
            print(Fore.LIGHTGREEN_EX + f"Moved: {file_name}")
        except (shutil.Error, Exception) as e:
            print(Fore.LIGHTRED_EX + f"Error Moving {file_name}: {e}")

    if destination_directory == AUTOEXEC_DIR:
        key_file_path = os.path.join("/storage/emulated/0/RonixExploit", "key.key")
        try:
            with open(key_file_path, 'w') as key_file:
                key_file.write("dqaDiYVhDfIqVuwxnRVJJsYMVLiKyKJA")
            print(Fore.LIGHTGREEN_EX + f"Created key.key in /storage/emulated/0/RonixExploit")
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"Error Creating key.key: {e}")

_session = None

def get_requests_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})
    return _session

def download_file_with_progress(url, destination):
    print(Fore.LIGHTBLUE_EX + f"Downloading From {url}...")
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
        print(Fore.LIGHTGREEN_EX + f"Downloaded {os.path.basename(destination)} Successfully")
        return True
    except requests.exceptions.Timeout:
        print(Fore.LIGHTRED_EX + f"Timeout Error Downloading {url}. Connection Too Slow Or Blocked")
        if os.path.exists(destination):
            os.remove(destination)
        return False
    except requests.exceptions.RequestException as e:
        print(Fore.LIGHTRED_EX + f"Error Downloading {url}: {e}")
        if os.path.exists(destination):
            os.remove(destination)
        return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Unknown Error Downloading {url}: {e}")
        if os.path.exists(destination):
            os.remove(destination)
        return False

def extract_zip_file(zip_path, extract_to_dir):
    print(Fore.LIGHTBLUE_EX + f"Extracting {os.path.basename(zip_path)} To {extract_to_dir}...")

    if os.path.exists(extract_to_dir):
        try:
            print(Fore.LIGHTYELLOW_EX + f"Deleting Old Directory: {extract_to_dir}")
            shutil.rmtree(extract_to_dir)
        except OSError as e:
            print(Fore.LIGHTRED_EX + f"Error Deleting Old Directory {extract_to_dir}: {e}")
            return False
    
    try:
        os.makedirs(extract_to_dir)
    except OSError as e:
        print(Fore.LIGHTRED_EX + f"Error Creating Destination Directory {extract_to_dir}: {e}")
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
                print(Fore.LIGHTYELLOW_EX + f"Detected Root Directory '{extracted_items[0]}', Moving Contents...")
                for item in os.listdir(source_path):
                    shutil.move(os.path.join(source_path, item), extract_to_dir)
            else:
                print(Fore.LIGHTYELLOW_EX + f"Moving Files Directly From Temporary Directory...")
                for item in os.listdir(temp_extract_dir):
                    shutil.move(os.path.join(temp_extract_dir, item), extract_to_dir)

        print(Fore.LIGHTGREEN_EX + f"Extraction Successful")
        return True
    except zipfile.BadZipFile:
        print(Fore.LIGHTRED_EX + f"Corrupted Zip File: {zip_path}")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error Extracting {zip_path}: {e}")
        return False
    finally:
        if os.path.exists(temp_extract_dir):
            try:
                shutil.rmtree(temp_extract_dir)
                print(Fore.LIGHTCYAN_EX + f"Cleaned Up Temporary Directory")
            except OSError as e:
                print(Fore.LIGHTRED_EX + f"Error Cleaning Up Temporary Directory {temp_extract_dir}: {e}")

def download_and_prepare_repository(update=False):
    clear_screen()
    
    if update and os.path.exists(ZIP_PATH):
        print(Fore.LIGHTYELLOW_EX + f"Deleting Old Zip File: {ZIP_PATH}...")
        try:
            os.remove(ZIP_PATH)
            print(Fore.LIGHTGREEN_EX + f"Deleted Old Zip File")
        except OSError as e:
            print(Fore.LIGHTRED_EX + f"Error Deleting Old Zip File: {e}")
            return False
            
    if not os.path.exists(ZIP_PATH):
        if not download_file_with_progress(REPO_URL, ZIP_PATH):
            return False

    if not extract_zip_file(ZIP_PATH, EXTRACTED_DIR):
        return False
    
    return True

def perform_setup():
    clear_screen()
    print(Fore.LIGHTBLUE_EX + "Starting Setup Process...")

    if not check_root_permissions():
        print(Fore.LIGHTRED_EX + "Root Permissions Required. Please Grant Root Permissions To Termux And Try Again")
        return False
    else:
        print(Fore.LIGHTGREEN_EX + "Root Permissions Granted")
    
    disable_bloatware_apps()
    set_android_id()
    
    move_extracted_files(EXTRA_FILES, DOWNLOADS_DIR)
    move_extracted_files(AUTOEXEC_FILES, AUTOEXEC_DIR)
    
    all_apks_installed = True
    for apk_file, pkg_name in APKS.items():
        if not install_apk(apk_file, pkg_name):
            all_apks_installed = False
    
    return all_apks_installed

def main_menu():
    while True:
        clear_screen()
        print(Fore.LIGHTWHITE_EX + r"""
  _______           /\          ________         _________ .__  .__        __ 
  \       \ ____ ___  _____ __ _____)/______ \_____  \____  ____  \_  ___ \|  | |__| ____ |  | __
  /  _  _ \_/ __ \\ \/  /  |  \/  ___//  ___/  /  _  _ \/  _  _ \_/ __ \  /    \  \/|  | |  |/ ___\|  |/ /
 /  /_\  \ \  ___/ >  <|  |  /\___ \ \___ \  /  /_\  \ \  \_/  \  ___/  \    ___|  |_|  \  \___|  < 
 \_______  /\___  >__/\_ \____//____  >____  > \_______  /\____/\___  >  \______  /____/__|\___  >__26
         \/     \/      \/          \/     \/          \/          \/          \/          \/     \/
        """)
        print(Fore.LIGHTBLUE_EX + "[1] Setup (Initial Installation)")
        print(Fore.LIGHTMAGENTA_EX + "[2] Update (Download And Reinstall)")
        print(Fore.LIGHTRED_EX + "[3] Exit")
        
        choice = input(Fore.LIGHTWHITE_EX + "Please Select Your Setup Option: ")
        
        if choice == "1":
            print(Fore.LIGHTBLUE_EX + "\nStarting Installation...")
            if download_and_prepare_repository(update=False):
                if perform_setup():
                    print(Fore.LIGHTGREEN_EX + "\nInstallation Completed Successfully")
                else:
                    print(Fore.LIGHTRED_EX + "\nInstallation Failed. Please Check Errors Above")
            else:
                print(Fore.LIGHTRED_EX + "\nDownload Or Repository Preparation Failed")
            input(Fore.LIGHTWHITE_EX + "Press Enter To Return To Main Menu...")
        elif choice == "2":
            print(Fore.LIGHTBLUE_EX + "\nStarting Update...")
            if download_and_prepare_repository(update=True):
                if perform_setup():
                    print(Fore.LIGHTGREEN_EX + "\nUpdate Completed Successfully")
                else:
                    print(Fore.LIGHTRED_EX + "\nUpdate Failed. Please Check Errors Above")
            else:
                print(Fore.LIGHTRED_EX + "\nDownload Or Repository Preparation For Update Failed")
            input(Fore.LIGHTWHITE_EX + "Press Enter To Return To Main Menu...")
        elif choice == "3":
            print(Fore.LIGHTRED_EX + "Exiting...")
            sys.exit(0)
        else:
            input(Fore.LIGHTWHITE_EX + "Invalid Choice, Press Enter To Try Again...")

if __name__ == "__main__":
    main_menu()
