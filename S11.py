import os
import subprocess
import shutil
import zipfile
import sys
import ssl
import requests
from colorama import init
from tqdm import tqdm
import concurrent.futures

init(autoreset=True)

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
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    except Exception:
        return None

def check_root_permissions():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False
    except Exception:
        return False

def is_package_installed(pkg_name):
    package_dir = os.path.join("/data/data", pkg_name)
    return os.path.isdir(package_dir)

def disable_play_store():
    run_command(["pm", "disable-user", "--user", "0", "com.android.vending"], check_success=True)

def disable_old_launcher():
    run_command(["pm", "disable-user", "--user", "0", "com.og.launcher"], check_success=True)

def set_android_id():
    run_command(["settings", "put", "secure", "android_id", ANDROID_ID], check_success=True)

def set_default_launcher(pkg_name):
    try:
        run_command(["pm", "clear-preferred-activities", "--user", "0"], check_success=True)
        launcher_cmd = [
            "am", "set-preferred-activity",
            "--user", "0",
            "-a", "android.intent.action.MAIN",
            "-c", "android.intent.category.HOME",
            "-c", "android.intent.category.DEFAULT",
            "-n", f"{pkg_name}/.MainActivity"
        ]
        return run_command(launcher_cmd, check_success=True) is not None
    except Exception:
        return False

def install_apk(apk_file, pkg_name):
    apk_path = os.path.join(EXTRACTED_DIR, apk_file)
    if is_package_installed(pkg_name):
        if pkg_name == "com.mi.android.globallaunches":
            set_default_launcher(pkg_name)
        return True
    if not os.path.exists(apk_path):
        return False
    try:
        install_cmd = ["pm", "install", "-r", "--full", apk_path]
        if run_command(install_cmd, check_success=True):
            if pkg_name == "com.mi.android.globallaunches":
                set_default_launcher(pkg_name)
            return True
        return False
    except Exception:
        return False

def allow_unknown_sources(pkg_name):
    run_command(["settings", "put", "secure", "install_non_market_apps", "1"], check_success=True)

def move_extracted_files(files_to_move, destination_directory):
    try:
        if destination_directory == AUTOEXEC_DIR:
            if os.path.exists(AUTOEXEC_DIR):
                shutil.rmtree(AUTOEXEC_DIR)
            os.makedirs(AUTOEXEC_DIR)
        else:
            os.makedirs(destination_directory, exist_ok=True)
    except OSError:
        return
    for file_name in files_to_move:
        source_path = os.path.join(EXTRACTED_DIR, file_name)
        destination_path = os.path.join(destination_directory, file_name)
        if not os.path.exists(source_path):
            continue
        try:
            if os.path.exists(destination_path):
                os.remove(destination_path)
            shutil.move(source_path, destination_path)
        except (shutil.Error, Exception):
            continue

_session = None

def get_requests_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})
    return _session

def download_file_with_progress(url, destination):
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
        return True
    except requests.exceptions.Timeout:
        if os.path.exists(destination):
            os.remove(destination)
        return False
    except requests.exceptions.RequestException:
        if os.path.exists(destination):
            os.remove(destination)
        return False
    except Exception:
        if os.path.exists(destination):
            os.remove(destination)
        return False

def extract_zip_file(zip_path, extract_to_dir):
    if os.path.exists(extract_to_dir):
        try:
            shutil.rmtree(extract_to_dir)
        except OSError:
            return False
    try:
        os.makedirs(extract_to_dir)
    except OSError:
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
                for item in os.listdir(source_path):
                    shutil.move(os.path.join(source_path, item), extract_to_dir)
            else:
                for item in os.listdir(temp_extract_dir):
                    shutil.move(os.path.join(temp_extract_dir, item), extract_to_dir)
        return True
    except zipfile.BadZipFile:
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return False
    except Exception:
        return False
    finally:
        if os.path.exists(temp_extract_dir):
            try:
                shutil.rmtree(temp_extract_dir)
            except OSError:
                pass

def download_and_prepare_repository(update=False):
    clear_screen()
    if update and os.path.exists(ZIP_PATH):
        try:
            os.remove(ZIP_PATH)
        except OSError:
            return False
    if not os.path.exists(ZIP_PATH):
        if not download_file_with_progress(REPO_URL, ZIP_PATH):
            return False
    if not extract_zip_file(ZIP_PATH, EXTRACTED_DIR):
        return False
    return True

def perform_setup():
    clear_screen()
    if not check_root_permissions():
        return False
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
        choice = input()
        if choice == "1":
            if download_and_prepare_repository(update=False):
                perform_setup()
            input()
        elif choice == "2":
            if download_and_prepare_repository(update=True):
                perform_setup()
            input()
        elif choice == "3":
            sys.exit(0)
        else:
            input()

if __name__ == "__main__":
    main_menu()
