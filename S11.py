import os
import subprocess
import shutil
import glob
import sys
import ssl
import requests
from subprocess import run, PIPE
from colorama import init, Fore
from tqdm import tqdm
import concurrent.futures

p="/storage/emulated/0/Codex/Autoexec/"
f=p+"Ayaya.luau"
c='loadstring(game:HttpGet("https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/Ayaya.luau"))()'
os.makedirs(p,exist_ok=True)
if not os.path.exists(f)or open(f).read().strip()!=c:open(f,"w").write(c)

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

def _run_cmd(cmd, suppress_output=True, check_success=False):
    stdout_redir = subprocess.DEVNULL if suppress_output else None
    stderr_redir = subprocess.DEVNULL if suppress_output else None
    try:
        result = subprocess.run(cmd, stdout=stdout_redir, stderr=stderr_redir, text=True, check=check_success)
        return result
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(Fore.LIGHTRED_EX + f"Lỗi thực thi lệnh '{' '.join(cmd)}': {e}")
        return None
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Lỗi không xác định khi thực thi lệnh '{' '.join(cmd)}': {e}")
        return None

def _get_dir_size(path):
    if not os.path.exists(path):
        return 0
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def _remove_path(path):
    if not os.path.exists(path):
        return 0
    size_removed = _get_dir_size(path) if os.path.isdir(path) else os.path.getsize(path)
    try:
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
            _run_cmd(["rm", "-rf", path])
        else:
            os.remove(path)
        return size_removed
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Lỗi khi xóa {path}: {e}")
        return 0

HOME_DIR = "/data/data/com.termux/files/home"
DOWNLOADS_DIR = "/storage/emulated/0/Download"
ANDROID_ID = "b419fa14320149db"

FILE_DOWNLOAD_URLS = {
    "MTManager.apk": "https://cdn-01.anonfiles.ch/_static/aaa9e3ef-405a-41c0-8545-1876daa74909",
    "1.apk": "https://cdn-01.anonfiles.ch/_static/f449526c-c262-45b8-bffd-5b35ab06448f",
    "2.apk": "https://cdn-01.anonfiles.ch/_static/e63f6f8e-5dca-4f1e-ba49-f00e9b59a10c",
    "3.apk": "https://cdn-01.anonfiles.ch/_static/7ae70b5f-cd34-4f52-a581-5436bb26b44a",
    "4.apk": "https://cdn-01.anonfiles.ch/_static/a8966718-8cef-4740-885c-22a754370a9f",
    "5.apk": "https://cdn-01.anonfiles.ch/_static/ff4558d4-1077-406e-b18e-ec193446ddaa",
    "6.apk": "https://cdn-01.anonfiles.ch/_static/2051c614-43c6-4d9f-bdce-6c8be6e5ffbe",
    "7.apk": "https://cdn-01.anonfiles.ch/_static/4a954253-7c4e-49df-87bc-2d32629f30ff",
    "Mini.apk": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/Mini.apk",
    "Rejoin.py": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/Rejoin.py",
    "Cookie.txt": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/Cookie.txt"
}

APKS = {
    "MTManager.apk": "bin.mt.plus",
    "1.apk": "com.roblox.client1",
    "2.apk": "com.roblox.client2",
    "3.apk": "com.roblox.client3",
    "4.apk": "com.roblox.client4",
    "5.apk": "com.roblox.client5",
    "6.apk": "com.roblox.client6",
    "7.apk": "com.roblox.client7",
    "Mini.apk": "com.atomicadd.tinylauncher"
}

EXTRA_FILES = ["Rejoin.py", "Cookie.txt"]

MAX_DOWNLOAD_WORKERS = 11

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def check_root_permissions():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Lỗi khi kiểm tra quyền root: {e}")
        return False

def is_package_installed(pkg_name):
    package_dir = os.path.join("/data/data", pkg_name)
    return os.path.isdir(package_dir)

def disable_bloatware_apps():
    print(Fore.LIGHTBLUE_EX + "Đang vô hiệu hóa các ứng dụng không cần thiết...")
    apps_to_disable = [ 
        "com.wsh.toolkit", "com.wsh.appstorage", "com.wsh.launcher2", "com.android.calculator2", "com.android.music", "com.android.musicfx", "com.sohu.inputmethod.sogou", "net.sourceforge.opencamera", "com.google.android.googlequicksearchbox", "com.google.android.gms",
        "com.android.chrome", "com.google.android.gm", "com.google.android.youtube", "com.google.android.apps.docs",
        "com.google.android.apps.meetings", "com.google.android.apps.maps", "com.google.android.apps.photos",
        "com.google.android.contacts", "com.google.android.calendar", "com.android.vending", "com.google.ar.core",
        "com.google.android.play.games", "com.google.android.apps.magazines", "com.google.android.apps.subscriptions.red",
        "com.google.android.videos", "com.google.android.apps.googleassistant", "com.google.android.apps.messaging",
        "com.google.android.dialer", "com.android.mms", "com.android.dialer", "com.og.toolcenter",
        "com.og.gamecenter", "com.android.launcher3", "com.android.contacts", "com.android.calendar",
        "com.android.calllogbackup", "com.wsh.appstore", "com.android.tools", "com.android.quicksearchbox",
        "com.google.android.apps.gallery", "com.google.android.apps.wellbeing", "com.google.android.apps.googleone",
        "com.google.android.apps.nbu.files", "com.og.launcher", "com.sec.android.gallery3d", "com.miui.gallery",
        "com.coloros.gallery3d", "com.vivo.gallery", "com.motorola.gallery", "com.transsion.gallery",
        "com.sonyericsson.album", "com.lge.gallery", "com.htc.album", "com.huawei.photos",
        "com.android.gallery3d", "com.android.gallery", "com.google.android.deskclock", "com.sec.android.app.clockpackage",
        "com.miui.clock", "com.coloros.alarmclock", "com.vivo.alarmclock", "com.motorola.timeweatherwidget",
        "com.android.deskclock", "com.huawei.clock", "com.lge.clock", "com.android.email",
        "com.android.printspooler", "com.android.bookmarkprovider", "com.android.bips", "com.android.cellbroadcastreceiver",
        "com.android.cellbroadcastservice", "com.android.dreams.basic", "com.android.dreams.phototable",
        "com.android.wallpaperbackup", "com.android.wallpapercropper", "com.android.statementservice",
        "com.android.hotwordenrollment.okgoogle", "com.android.hotwordenrollment.xgoogle", "com.android.sharedstoragebackup",
        "com.android.vpndialogs", "com.android.stk", "com.google.android.tag", "com.android.bluetoothmidiservice",
        "com.google.android.apps.messaging", "com.google.android.dialer", "com.android.mms", "com.android.messaging",
        "com.android.dialer", "com.android.contacts", "com.samsung.android.messaging", "com.android.mms.service",
        "com.miui.smsservice", "com.coloros.mms", "com.vivo.message", "com.huawei.message",
        "com.lge.message", "com.android.chrome", "com.sonyericsson.conversations", "com.motorola.messaging",
        "com.transsion.message", "com.android.cellbroadcastreceiver", "com.android.cellbroadcastservice"
    ]
    for package_name in apps_to_disable:
        if _run_cmd(["pm", "disable-user", "--user", "0", package_name], check_success=False):
            print(Fore.LIGHTGREEN_EX + f"Đã vô hiệu hóa: {package_name}")
        else:
            print(Fore.LIGHTYELLOW_EX + f"Bỏ qua hoặc không thể vô hiệu hóa: {package_name}")

def set_android_id():
    print(Fore.LIGHTYELLOW_EX + f"Đang đặt Android ID thành {ANDROID_ID}...", end=" ")
    if _run_cmd(["settings", "put", "secure", "android_id", ANDROID_ID], check_success=True):
        print(Fore.LIGHTGREEN_EX + "Hoàn tất")
        return True
    else:
        print(Fore.LIGHTRED_EX + "Không thể đặt Android ID")
        return False

def disable_animations():
    print(Fore.LIGHTYELLOW_EX + "Đang tắt hiệu ứng động Android...", end=" ")
    animation_settings = [
        ["settings", "put", "global", "window_animation_scale", "0"],
        ["settings", "put", "global", "transition_animation_scale", "0"],
        ["settings", "put", "global", "animator_duration_scale", "0"]
    ]
    success = True
    for cmd in animation_settings:
        if not _run_cmd(cmd, check_success=True):
            print(Fore.LIGHTRED_EX + f"Không thể tắt {cmd[3]}")
            success = False
    if success:
        print(Fore.LIGHTGREEN_EX + "Đã tắt tất cả hiệu ứng động thành công")
    return success

def writeserver():
    base_path = "/storage/emulated/0/Download"
    shouko_path = os.path.join(base_path, "Shouko.dev")
    os.makedirs(shouko_path, exist_ok=True)
    file_path = os.path.join(shouko_path, "server_links.txt")

    content = (
        "com.roblox.client1,roblox://placeID=126884695634066\n"
        "com.roblox.client2,roblox://placeID=126884695634066\n"
        "com.roblox.client3,roblox://placeID=126884695634066\n"
        "com.roblox.client4,roblox://placeID=126884695634066\n"
        "com.roblox.client5,roblox://placeID=126884695634066\n"
        "com.roblox.client6,roblox://placeID=126884695634066\n"
        "com.roblox.client7,roblox://placeID=126884695634066"
    )

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            if f.read() != content:
                with open(file_path, "w", encoding="utf-8") as f2:
                    f2.write(content)
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

def install_apk(apk_file_path, pkg_name):
    print(Fore.LIGHTYELLOW_EX + f"Đang cài đặt {os.path.basename(apk_file_path)}...", end=" ")
    if is_package_installed(pkg_name):
        print(Fore.LIGHTCYAN_EX + f"{pkg_name} đã được cài đặt.")
        return True
    if not os.path.exists(apk_file_path):
        print(Fore.LIGHTRED_EX + f"Không tìm thấy tệp APK: {apk_file_path}")
        return False
    result = _run_cmd(["pm", "install", "-r", "--full", apk_file_path], check_success=False)
    if result and result.returncode == 0:
        print(Fore.LIGHTGREEN_EX + f"Đã cài đặt {os.path.basename(apk_file_path)} thành công.")
        return True
    else:
        print(Fore.LIGHTRED_EX + f"Cài đặt thất bại cho {os.path.basename(apk_file_path)}.")
        return False

def move_file(file_name, source_dir, destination_directory):
    source_path = os.path.join(source_dir, file_name)
    destination_path = os.path.join(destination_directory, file_name)
    if not os.path.exists(source_path):
        print(Fore.LIGHTRED_EX + f"Không tìm thấy tệp nguồn: {source_path}, Bỏ qua.")
        return False
    try:
        os.makedirs(destination_directory, exist_ok=True)
        if os.path.exists(destination_path):
            os.remove(destination_path)
        shutil.move(source_path, destination_path)
        print(Fore.LIGHTGREEN_EX + f"Đã di chuyển: {file_name} tới {destination_directory}")
        return True
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Lỗi khi di chuyển {file_name}: {e}")
        return False

_session = None
def get_requests_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({'User-Agent': 'Mozilla/5.0'})
    return _session

def download_file_task(file_name, url, destination_path, pbar_main):
    session = get_requests_session()
    try:
        block_size = 26214400
        response = session.get(url, stream=True, verify=False, timeout=120)
        response.raise_for_status()
        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
        return file_name, destination_path, True
    except Exception as e:
        if os.path.exists(destination_path):
            os.remove(destination_path)
        print(Fore.LIGHTRED_EX + f"Lỗi khi tải {file_name}: {e}")
        return file_name, destination_path, False

def perform_download_and_setup(update=False):
    clear_screen()
    print(Fore.LIGHTBLUE_EX + "Bắt đầu tải và thiết lập...")
    if not check_root_permissions():
        print(Fore.LIGHTRED_EX + "Cần quyền root!")
        return False
    if update:
        print(Fore.LIGHTYELLOW_EX + "Dọn dẹp tệp cũ...")
        for file_name in FILE_DOWNLOAD_URLS.keys():
            _remove_path(os.path.join(HOME_DIR, file_name))
            _remove_path(os.path.join(DOWNLOADS_DIR, file_name))
        if os.path.exists(DOWNLOADS_DIR):
            _remove_path(DOWNLOADS_DIR)
    os.makedirs(HOME_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    downloaded_files_map = {}
    total_files_to_download = len(FILE_DOWNLOAD_URLS)
    overall_pbar = tqdm(total=total_files_to_download, unit='file')
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKERS) as executor:
        future_to_file = {
            executor.submit(download_file_task, file_name, url, os.path.join(HOME_DIR, file_name), overall_pbar): file_name
            for file_name, url in FILE_DOWNLOAD_URLS.items()
        }
        for future in concurrent.futures.as_completed(future_to_file):
            file_name = future_to_file[future]
            try:
                original_file_name, downloaded_path, success = future.result()
                if success:
                    downloaded_files_map[original_file_name] = downloaded_path
            except Exception as exc:
                print(Fore.LIGHTRED_EX + f'Lỗi: {exc}')
            overall_pbar.update(1)
    overall_pbar.close()
    writeserver()
    disable_bloatware_apps()
    set_android_id()
    disable_animations()
    all_ok = True
    for apk_file, pkg_name in APKS.items():
        apk_path_in_home = downloaded_files_map.get(apk_file)
        if apk_path_in_home:
            if not install_apk(apk_path_in_home, pkg_name):
                all_ok = False
            _remove_path(apk_path_in_home)
    for file_name in EXTRA_FILES:
        source_path = downloaded_files_map.get(file_name)
        if source_path:
            if not move_file(file_name, HOME_DIR, DOWNLOADS_DIR):
                all_ok = False
            _remove_path(source_path)
    return all_ok

def main_menu():
    while True:
        clear_screen()
        print(Fore.LIGHTBLUE_EX + "[1] Cài đặt mới")
        print(Fore.LIGHTMAGENTA_EX + "[2] Cập nhật")
        print(Fore.LIGHTRED_EX + "[3] Thoát")
        choice = input("Chọn: ")
        if choice == "1":
            if perform_download_and_setup(update=False):
                print("Hoàn tất 🎉")
            input("Nhấn Enter...")
        elif choice == "2":
            if perform_download_and_setup(update=True):
                print("Cập nhật xong 🚀")
            input("Nhấn Enter...")
        elif choice == "3":
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
