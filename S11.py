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
AUTOEXEC_DIR = "/storage/emulated/0/Cryptic/Autoexec/"
ANDROID_ID = "b419fa14320149db"

FILE_DOWNLOAD_URLS = {
    "MTManager.apk": "https://cdn-01.anonfiles.ch/_static/aaa9e3ef-405a-41c0-8545-1876daa74909",
    "1.apk": "https://cdn-01.anonfiles.ch/_static/8120b3aa-efb1-442d-8167-84cf6bf556b1",
    "2.apk": "https://cdn-01.anonfiles.ch/_static/017a0d68-f9d2-4e83-b9d9-c25321a6f6a0",
    "3.apk": "https://cdn-01.anonfiles.ch/_static/40aad0b4-42f0-4742-95f7-01dbc8c10f0a",
    "4.apk": "https://cdn-01.anonfiles.ch/_static/503b55d4-f863-45dc-af48-2587094784a0",
    "5.apk": "https://cdn-01.anonfiles.ch/_static/e3916f15-5b87-4b1e-a553-4a4e78da6ffa",
    "6.apk": "https://cdn-01.anonfiles.ch/_static/fc1d4d8b-6f96-4dac-a564-e6a81205d634",
    "Via.apk": "https://cdn-01.anonfiles.ch/_static/f9f5ddc1-fb31-4b80-9b4a-80630af18619",
    "Mini.apk": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/Mini.apk",
    "config-change.json": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/config-change.json",
    "Rejoin.py": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/Rejoin.py",
    "Cookie.txt": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/Cookie.txt",
    "con_cac_ba_may.luau": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/con_cac_ba_may.luau",
    "check_info.luau": "https://raw.githubusercontent.com/ENMN11/NexusHideout/refs/heads/main/check_info.luau"
}

APKS = {
    "MTManager.apk": "bin.mt.plus",
    "Via.apk": "mark.via.gp",
    "1.apk": "com.roblox.client1",
    "2.apk": "com.roblox.client2",
    "3.apk": "com.roblox.client3",
    "4.apk": "com.roblox.client4",
    "5.apk": "com.roblox.client5",
    "6.apk": "com.roblox.client6",
    "Mini.apk": "com.atomicadd.tinylauncher"
}

EXTRA_FILES = ["config-change.json", "Rejoin.py", "Cookie.txt"]
AUTOEXEC_FILES = ["con_cac_ba_may.luau", "check_info.luau"]

MAX_DOWNLOAD_WORKERS = 13

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

def disable_bloatware_apps(): # Đã đổi tên hàm từ uninstall_bloatware_apps
    print(Fore.LIGHTBLUE_EX + "Đang vô hiệu hóa các ứng dụng không cần thiết...")
    apps_to_disable = [ # Đã đổi tên biến từ apps_to_uninstall
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

    for package_name in apps_to_disable: # Đã đổi tên biến
        # Đã thay đổi lệnh từ 'uninstall' thành 'disable'
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

# HÀM clean_junk_files ĐÃ ĐƯỢC XÓA BỎ HOÀN TOÀN TRONG CÁC PHIÊN BẢN TRƯỚC

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
        if result and result.stderr:
            print(Fore.LIGHTRED_EX + f"Thông báo lỗi: {result.stderr.strip()}")
        return False

def move_file(file_name, source_dir, destination_directory):
    source_path = os.path.join(source_dir, file_name)
    destination_path = os.path.join(destination_directory, file_name)
    
    if not os.path.exists(source_path):
        print(Fore.LIGHTRED_EX + f"Không tìm thấy tệp nguồn: {source_path}, Bỏ qua việc di chuyển.")
        return False
        
    try:
        os.makedirs(destination_directory, exist_ok=True)
        
        if os.path.exists(destination_path):
            os.remove(destination_path)
        shutil.move(source_path, destination_path)
        print(Fore.LIGHTGREEN_EX + f"Đã di chuyển: {file_name} tới {destination_directory}")
        return True
    except (shutil.Error, Exception) as e:
        print(Fore.LIGHTRED_EX + f"Lỗi khi di chuyển {file_name} từ {source_dir} tới {destination_directory}: {e}")
        return False

_session = None
def get_requests_session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})
    return _session

def download_file_task(file_name, url, destination_path, pbar_main):
    session = get_requests_session()
    try:
        block_size = 5242880
        response = session.get(url, stream=True, verify=False, timeout=120)
        response.raise_for_status()

        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    
        return file_name, destination_path, True
    except requests.exceptions.Timeout:
        print(Fore.LIGHTRED_EX + f"Lỗi timeout khi tải {file_name} từ {url}. Kết nối quá chậm hoặc bị chặn.")
        if os.path.exists(destination_path):
            os.remove(destination_path)
        return file_name, destination_path, False
    except requests.exceptions.RequestException as e:
        print(Fore.LIGHTRED_EX + f"Lỗi tải xuống {file_name} từ {url}: {e}")
        if os.path.exists(destination_path):
            os.remove(destination_path)
        return file_name, destination_path, False
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Lỗi không xác định khi tải xuống {file_name} từ {url}: {e}")
        if os.path.exists(destination_path):
            os.remove(destination_path)
        return file_name, destination_path, False

def perform_download_and_setup(update=False):
    clear_screen()
    print(Fore.LIGHTBLUE_EX + "Đang bắt đầu quá trình tải xuống và thiết lập...")

    if not check_root_permissions():
        print(Fore.LIGHTRED_EX + "Cần quyền root. Vui lòng cấp quyền root cho Termux và thử lại.")
        return False
    else:
        print(Fore.LIGHTGREEN_EX + "Đã cấp quyền root.")
    
    if update:
        print(Fore.LIGHTYELLOW_EX + "Đang dọn dẹp các tệp đã tải xuống trước đây...")
        for file_name in FILE_DOWNLOAD_URLS.keys():
            _remove_path(os.path.join(HOME_DIR, file_name))
            _remove_path(os.path.join(DOWNLOADS_DIR, file_name))
            _remove_path(os.path.join(AUTOEXEC_DIR, file_name))
        
        if os.path.exists(DOWNLOADS_DIR):
            _remove_path(DOWNLOADS_DIR)
            print(Fore.LIGHTCYAN_EX + f"Đã dọn dẹp thư mục cũ: {DOWNLOADS_DIR}.")
        if os.path.exists(AUTOEXEC_DIR):
            _remove_path(AUTOEXEC_DIR)
            print(Fore.LIGHTCYAN_EX + f"Đã dọn dẹp thư mục cũ: {AUTOEXEC_DIR}.")
    
    os.makedirs(HOME_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    os.makedirs(AUTOEXEC_DIR, exist_ok=True)

    downloaded_files_map = {}
    print(Fore.LIGHTBLUE_EX + "\nĐang khởi tạo tải xuống tệp đồng thời...")
    
    total_files_to_download = len(FILE_DOWNLOAD_URLS)
    overall_pbar = tqdm(total=total_files_to_download, unit='file', desc="Tổng tiến trình tải xuống", ncols=100)

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
                else:
                    print(Fore.LIGHTRED_EX + f"Tải xuống thất bại cho {original_file_name}. Sẽ không xử lý tiếp.")
            except Exception as exc:
                print(Fore.LIGHTRED_EX + f'Tệp {file_name} gây ra một ngoại lệ: {exc}')
            overall_pbar.update(1)
    
    overall_pbar.close()
    
    if len(downloaded_files_map) != total_files_to_download:
        print(Fore.LIGHTRED_EX + "Không phải tất cả các tệp đều được tải xuống thành công. Hủy thiết lập.")
        return False

    disable_bloatware_apps()
    set_android_id()
    disable_animations()
    
    all_operations_successful = True

    print(Fore.LIGHTBLUE_EX + "\nĐang cài đặt các APK...")
    for apk_file, pkg_name in APKS.items():
        apk_path_in_home = downloaded_files_map.get(apk_file)
        if apk_path_in_home:
            if not install_apk(apk_path_in_home, pkg_name):
                all_operations_successful = False
            _remove_path(apk_path_in_home)
            print(Fore.LIGHTCYAN_EX + f"Đã xóa APK tạm thời: {apk_file}")
        else:
            print(Fore.LIGHTRED_EX + f"Không tìm thấy tệp APK {apk_file} trong các tệp đã tải xuống. Bỏ qua cài đặt.")
            all_operations_successful = False

    print(Fore.LIGHTBLUE_EX + "\nĐang di chuyển các tệp bổ sung (Extra Files)...")
    for file_name in EXTRA_FILES:
        source_path = downloaded_files_map.get(file_name)
        if source_path:
            if not move_file(file_name, HOME_DIR, DOWNLOADS_DIR):
                all_operations_successful = False
            _remove_path(source_path)
        else:
            print(Fore.LIGHTRED_EX + f"Tệp {file_name} chưa được tải xuống, không thể di chuyển.")
            all_operations_successful = False

    print(Fore.LIGHTBLUE_EX + "\nĐang di chuyển các tệp Autoexec...")
    for file_name in AUTOEXEC_FILES:
        source_path = downloaded_files_map.get(file_name)
        if source_path:
            if not move_file(file_name, HOME_DIR, AUTOEXEC_DIR):
                all_operations_successful = False
            _remove_path(source_path)
        else:
            print(Fore.LIGHTRED_EX + f"Tệp {file_name} chưa được tải xuống, không thể di chuyển.")
            all_operations_successful = False

    return all_operations_successful

def main_menu():
    while True:
        clear_screen()
        print(Fore.LIGHTWHITE_EX + r"""
  _______          /\           ________         _________ .__  .__          __ 
  \       \ ____ ___  _____ __ _____)/______ \_____  \____  ____  \_  ___ \|  | |__| ____ |  | __
  /  _  _ \_/ __ \\ \/  /  |  \/  ___//  ___/  /  _  _ \/  _  _ \/  _  _ \_/ __ \  /    \  \/|  | |  |/ ___\|  |/ /
 /  /_\  \ \  ___/ >  <|  |  /\___ \ \___ \  /  /_\  \ \  \_/  \  ___/  \    ___|  |_|  \  \___|  < 
 \_______  /\___  >__/\_ \____//____  >____  > \_______  /\____/\___  >  \______  /____/__|\___  >__26
          \/     \/      \/          \/     \/          \/          \/           \/          \/     \/
        """)
        print(Fore.LIGHTBLUE_EX + "[1] Cài đặt (Lần đầu tiên)")
        print(Fore.LIGHTMAGENTA_EX + "[2] Cập nhật (Tải xuống và cài đặt lại)")
        print(Fore.LIGHTRED_EX + "[3] Thoát")
        
        choice = input(Fore.LIGHTWHITE_EX + "Vui lòng chọn tùy chọn thiết lập của bạn: ")
        
        if choice == "1":
            print(Fore.LIGHTBLUE_EX + "\nĐang bắt đầu cài đặt...")
            if perform_download_and_setup(update=False):
                print(Fore.LIGHTGREEN_EX + "\nCài đặt hoàn tất thành công 🎉")
            else:
                print(Fore.LIGHTRED_EX + "\nCài đặt thất bại. Vui lòng kiểm tra lỗi ở trên ❌")
            input(Fore.LIGHTWHITE_EX + "Nhấn Enter để quay lại Menu chính...")
        elif choice == "2":
            print(Fore.LIGHTBLUE_EX + "\nĐang bắt đầu cập nhật...")
            if perform_download_and_setup(update=True):
                print(Fore.LIGHTGREEN_EX + "\nCập nhật hoàn tất thành công 🚀")
            else:
                print(Fore.LIGHTRED_EX + "\nCập nhật thất bại. Vui lòng kiểm tra lỗi ở trên ⚠️")
            input(Fore.LIGHTWHITE_EX + "Nhấn Enter để quay lại Menu chính...")
        elif choice == "3":
            print(Fore.LIGHTRED_EX + "Đang thoát... Hẹn gặp lại! 👋")
            sys.exit(0)
        else:
            input(Fore.LIGHTWHITE_EX + "Lựa chọn không hợp lệ, nhấn Enter để thử lại...")

if __name__ == "__main__":
    main_menu()
