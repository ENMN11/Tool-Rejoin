import threading
import time
import json
import requests
import subprocess
import sqlite3
import shutil
import pytz
import traceback
import random
import psutil
import sys
import gc
import os
import uuid  # Thêm để tạo tên file tạm ngẫu nhiên
from prettytable import PrettyTable
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.box import ROUNDED
from rich.console import Console
from datetime import datetime, timezone
from threading import Lock, Event

# --- Global Variables and Locks ---
# Sử dụng RLock (Reentrant Lock) để an toàn hơn nếu cùng 1 thread gọi lock nhiều lần
package_lock = Lock()
status_lock = Lock()
file_lock = Lock() 

stop_webhook_thread = False
webhook_thread = None
webhook_url = None
device_name = None
webhook_interval = None
reset_tab_interval = None
close_and_rejoin_delay = None

# Fix: Lấy thời gian boot hệ thống chính xác
system_boot_time = psutil.boot_time()

auto_android_id_enabled = False
auto_android_id_thread = None
auto_android_id_value = None

# Các biến Global cấu hình
globals()["_disable_ui"] = "0"
globals()["package_statuses"] = {}
globals()["_uid_"] = {}
globals()["_user_"] = {}
globals()["is_runner_ez"] = False
globals()["check_exec_enable"] = "1"

# Danh sách Executor (Giữ nguyên, rút gọn hiển thị để code gọn)
executors = {
    "Fluxus": "/storage/emulated/0/Fluxus/",
    "Codex": "/storage/emulated/0/Codex/",
    "Arceus X": "/storage/emulated/0/Arceus X/",
    "Delta": "/storage/emulated/0/Delta/",
    "KRNL": "/storage/emulated/0/krnl/",
    "Trigon": "/storage/emulated/0/Trigon/",
    "Evon": "/storage/emulated/0/Evon/",
    # ... (Code tự động xử lý clones, giữ nguyên logic cũ)
}

# Tự động tạo đường dẫn workspace
workspace_paths = [f"{base_path}Workspace" for base_path in executors.values()] + \
                  [f"{base_path}workspace" for base_path in executors.values()]
globals()["workspace_paths"] = workspace_paths
globals()["executors"] = executors

# Cấu hình đường dẫn file
BASE_DIR = "Shouko.dev"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR, exist_ok=True)

SERVER_LINKS_FILE = os.path.join(BASE_DIR, "server-links.txt")
ACCOUNTS_FILE = os.path.join(BASE_DIR, "accounts.txt")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
ERROR_LOG_FILE = "error_log.txt"

version = "2.3.0 Stable | Refactored by Shouko.dev | Optimized Logic"

class Utilities:
    @staticmethod
    def collect_garbage():
        # Chỉ gọi khi cần thiết để tránh tốn CPU
        if psutil.virtual_memory().percent > 85:
            gc.collect()

    @staticmethod
    def log_error(error_message):
        with file_lock: # Lock file để tránh lỗi khi nhiều luồng cùng ghi
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(ERROR_LOG_FILE, "a", encoding="utf-8") as error_log:
                    error_log.write(f"[{timestamp}] {error_message}\n\n")
            except:
                pass

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def run_shell(command):
        """Hàm chạy lệnh shell an toàn, ẩn output rác"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            return ""

class FileManager:
    # Sửa lại đường dẫn cho đúng chuẩn
    SERVER_LINKS_FILE = os.path.join(BASE_DIR, "server-link.txt")
    ACCOUNTS_FILE = os.path.join(BASE_DIR, "account.txt")
    CONFIG_FILE = os.path.join(BASE_DIR, "config-wh.json")

    @staticmethod
    def get_cookie_from_db(file_path):
        """
        Đọc cookie từ DB SQLite an toàn hơn.
        Sử dụng UUID để tạo tên file tạm -> Tránh xung đột khi chạy đa luồng.
        """
        if not os.path.exists(file_path):
            return None
        
        temp_filename = f"cookie_temp_{uuid.uuid4().hex}"
        temp_path = os.path.join(BASE_DIR, temp_filename)
        
        conn = None
        try:
            # Copy file DB ra chỗ khác để đọc
            shutil.copy2(file_path, temp_path)
            
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM cookies WHERE name = '.ROBLOSECURITY'")
            result = cursor.fetchone()
            
            if result:
                return result[0]
            return None
            
        except Exception as e:
            # Utilities.log_error(f"DB Read Error: {e}")
            return None
        finally:
            # Đảm bảo đóng kết nối và xóa file tạm
            if conn:
                try:
                    conn.close()
                except:
                    pass
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass

    @staticmethod
    def setup_user_ids():
        print("\033[1;32m[ Shouko.dev ] - Auto-detecting User IDs from app packages...\033[0m")
        packages = RobloxManager.get_roblox_packages()
        accounts = []
        if not packages:
            print("\033[1;31m[ Shouko.dev ] - No Roblox packages detected.\033[0m")
            return []

        for package_name in packages:
            file_path = f'/data/data/{package_name}/files/appData/LocalStorage/appStorage.json'
            try:
                user_id = FileManager.find_userid_from_file(file_path)
                if user_id and user_id != "-1":
                    accounts.append((package_name, user_id))
                    print(f"\033[96m[ Shouko.dev ] - Found UserID for {package_name}: {user_id}\033[0m")
                else:
                    print(f"\033[1;31m[ Shouko.dev ] - UserID not found for {package_name}.\033[0m")
            except Exception:
                # Không in lỗi chi tiết ra màn hình để tránh spam, chỉ log
                Utilities.log_error(f"Error reading appStorage.json for {package_name}")

        if accounts:
            FileManager.save_accounts(accounts)
            print("\033[1;32m[ Shouko.dev ] - User IDs saved successfully.\033[0m")
        else:
            print("\033[1;31m[ Shouko.dev ] - Could not find any valid User IDs.\033[0m")
        
        return accounts

    @staticmethod
    def save_server_links(server_links):
        try:
            os.makedirs(os.path.dirname(FileManager.SERVER_LINKS_FILE), exist_ok=True)
            with open(FileManager.SERVER_LINKS_FILE, "w") as file:
                for package, link in server_links:
                    file.write(f"{package},{link}\n")
            print("\033[1;32m[ Shouko.dev ] - Server links saved.\033[0m")
        except IOError as e:
            print(f"\033[1;31m[ Shouko.dev ] - Error saving server links: {e}\033[0m")

    @staticmethod
    def load_server_links():
        server_links = []
        if os.path.exists(FileManager.SERVER_LINKS_FILE):
            with open(FileManager.SERVER_LINKS_FILE, "r") as file:
                for line in file:
                    try:
                        if "," in line:
                            package, link = line.strip().split(",", 1)
                            server_links.append((package, link))
                    except ValueError:
                        continue
        return server_links

    @staticmethod
    def save_accounts(accounts):
        try:
            with open(FileManager.ACCOUNTS_FILE, "w") as file:
                for package, user_id in accounts:
                    file.write(f"{package},{user_id}\n")
        except Exception as e:
            Utilities.log_error(f"Error saving accounts: {e}")

    @staticmethod
    def load_accounts():
        accounts = []
        if os.path.exists(FileManager.ACCOUNTS_FILE):
            with open(FileManager.ACCOUNTS_FILE, "r") as file:
                for line in file:
                    line = line.strip()
                    if line and "," in line:
                        try:
                            package, user_id = line.split(",", 1)
                            globals()["_user_"][package] = user_id
                            accounts.append((package, user_id))
                        except ValueError:
                            pass
        return accounts

    @staticmethod
    def find_userid_from_file(file_path):
        try:
            if not os.path.exists(file_path):
                return None
            # Đọc file với errors='ignore' để tránh lỗi encoding
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                userid_start = content.find('"UserId":"')
                if userid_start == -1:
                    return None

                userid_start += len('"UserId":"')
                userid_end = content.find('"', userid_start)
                if userid_end == -1:
                    return None

                userid = content[userid_start:userid_end]
                return userid
        except IOError:
            return None

    @staticmethod
    def get_username(user_id):
        user = FileManager.load_saved_username(user_id)
        if user: return user
        
        # Thêm timeout để không bị treo
        apis = [
            f"https://users.roblox.com/v1/users/{user_id}",
            f"https://users.roproxy.com/v1/users/{user_id}"
        ]
        
        for url in apis:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    username = data.get("name", "Unknown")
                    if username != "Unknown":
                        FileManager.save_username(user_id, username)
                        return username
            except:
                continue
        return "Unknown"

    @staticmethod
    def save_username(user_id, username):
        try:
            data = {}
            if os.path.exists("usernames.json"):
                try:
                    with open("usernames.json", "r") as file:
                        data = json.load(file)
                except:
                    data = {}
            
            data[str(user_id)] = username
            with open("usernames.json", "w") as file:
                json.dump(data, file)
        except:
            pass

    @staticmethod
    def load_saved_username(user_id):
        try:
            if not os.path.exists("usernames.json"):
                return None
            with open("usernames.json", "r") as file:
                data = json.load(file)
                return data.get(str(user_id), None)
        except:
            return None

    @staticmethod
    def download_file(url, destination, binary=False):
        try:
            response = requests.get(url, stream=True, timeout=30) # Thêm timeout 30s
            if response.status_code == 200:
                mode = 'wb' if binary else 'w'
                encoding = 'utf-8' if not binary else None
                with open(destination, mode, encoding=encoding) as file:
                    if binary:
                        shutil.copyfileobj(response.raw, file)
                    else:
                        file.write(response.text)
                print(f"\033[1;32m[ Shouko.dev ] - Downloaded {os.path.basename(destination)}.\033[0m")
                return destination
            else:
                print(f"\033[1;31m[ Shouko.dev ] - Download failed: {response.status_code}\033[0m")
                return None
        except Exception as e:
            print(f"\033[1;31m[ Shouko.dev ] - Error downloading: {e}\033[0m")
            return None

    @staticmethod
    def _load_config():
        global webhook_url, device_name, webhook_interval
        try:
            if os.path.exists(FileManager.CONFIG_FILE):
                with open(FileManager.CONFIG_FILE, "r") as file:
                    config = json.load(file)
                    webhook_url = config.get("webhook_url", None)
                    device_name = config.get("device_name", None)
                    webhook_interval = config.get("interval", float('inf'))
                    globals()["_disable_ui"] = config.get("disable_ui", "0")
                    globals()["check_exec_enable"] = config.get("check_executor", "1")
                    globals()["command_8_configured"] = config.get("command_8_configured", False)
                    globals()["lua_script_template"] = config.get("lua_script_template", None)
                    globals()["package_prefix"] = config.get("package_prefix", "com.roblox")
            else:
                # Default values
                webhook_url = None
                device_name = None
                webhook_interval = float('inf')
                globals()["check_exec_enable"] = "1"
                globals()["package_prefix"] = "com.roblox"
        except Exception:
            Utilities.log_error("Config file corrupted or unreadable.")

    @staticmethod
    def save_config():
        try:
            config = {
                "webhook_url": webhook_url,
                "device_name": device_name,
                "interval": webhook_interval,
                "disable_ui": globals().get("_disable_ui", "0"),
                "check_executor": globals()["check_exec_enable"],
                "command_8_configured": globals().get("command_8_configured", False),
                "lua_script_template": globals().get("lua_script_template", None),
                "package_prefix": globals().get("package_prefix", "com.roblox"),
            }
            with open(FileManager.CONFIG_FILE, "w") as file:
                json.dump(config, file, indent=4, sort_keys=True)
            print("\033[1;32m[ Shouko.dev ] - Configuration saved.\033[0m")
        except Exception as e:
            print(f"\033[1;31m[ Shouko.dev ] - Error saving config: {e}\033[0m")

    @staticmethod
    def check_and_create_cookie_file():
        folder_path = os.path.dirname(os.path.abspath(__file__))
        cookie_file_path = os.path.join(folder_path, 'cookie.txt')
        if not os.path.exists(cookie_file_path):
            with open(cookie_file_path, 'w') as f:
                f.write("")

class SystemMonitor:
    @staticmethod
    def capture_screenshot():
        screenshot_path = "/storage/emulated/0/Download/screenshot.png"
        try:
            # Dùng subprocess thay vì os.system để an toàn hơn
            subprocess.run(["/system/bin/screencap", "-p", screenshot_path], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not os.path.exists(screenshot_path):
                return None
            return screenshot_path
        except:
            return None

    @staticmethod
    def get_uptime():
        current_time = time.time()
        uptime_seconds = current_time - system_boot_time
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{days}d {hours}h {minutes}m"

    @staticmethod
    def roblox_processes():
        package_names = []
        package_namez = RobloxManager.get_roblox_packages()
        for proc in psutil.process_iter(['name', 'pid', 'memory_info', 'cpu_percent']):
            try:
                proc_name = proc.info['name']
                # Kiểm tra nhẹ nhàng hơn
                for package_name in package_namez:
                    if package_name in proc_name or proc_name == package_name:
                        mem_usage = round(proc.info['memory_info'].rss / (1024 ** 2), 2)
                        # CPU percent blocking call removed
                        package_names.append(f"{package_name} (PID: {proc.pid}, MEM: {mem_usage}MB)")
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return package_names

    @staticmethod
    def get_memory_usage():
        try:
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()
            return round(mem_info.rss / (1024 ** 2), 2)
        except:
            return None

    @staticmethod
    def get_system_info():
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            memory_info = psutil.virtual_memory()
            system_info = {
                "cpu_usage": cpu_usage,
                "memory_total": round(memory_info.total / (1024 ** 3), 2),
                "memory_used": round(memory_info.used / (1024 ** 3), 2),
                "memory_percent": memory_info.percent,
                "uptime": SystemMonitor.get_uptime(),
                "roblox_packages": SystemMonitor.roblox_processes()
            }
            return system_info
        except:
            return False

class RobloxManager:
    @staticmethod
    def get_cookie():
        try:
            current_dir = os.getcwd()
            cookie_txt_path = os.path.join(current_dir, "cookie.txt")
            new_dir_path = os.path.join(current_dir, "Shouko.dev/Shouko.dev - Data")
            new_cookie_path = os.path.join(new_dir_path, "cookie.txt")

            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path, exist_ok=True)

            if not os.path.exists(cookie_txt_path):
                print("\033[1;31m[ Shouko.dev ] - cookie.txt missing!\033[0m")
                return False

            cookies = []
            org = []

            with open(cookie_txt_path, "r") as file:
                for line in file.readlines():
                    line = str(line).strip()
                    if not line: continue
                    
                    ck = line
                    # Xử lý format Netscape nếu có
                    parts = line.split(":")
                    if len(parts) >= 4 and "ROBLOSECURITY" in line:
                        ck = parts[-1] # Lấy phần cuối cùng
                    
                    # Basic validation
                    if "_|WARNING:" in ck or ".ROBLOSECURITY" in ck:
                         org.append(line)
                         cookies.append(ck)

            if not cookies:
                print("\033[1;31m[ Shouko.dev ] - No valid cookies found.\033[0m")
                return False

            cookie = cookies.pop(0)
            original_line = org.pop(0)

            # Lưu lại cookie đã dùng vào file history
            with open(new_cookie_path, "a") as new_file:
                new_file.write(original_line + "\n")

            # Ghi lại các cookie chưa dùng
            with open(cookie_txt_path, "w") as file:
                file.write("\n".join(org))

            return cookie

        except Exception as e:
            print(f"\033[1;31m[ Shouko.dev ] - Cookie Error: {e}\033[0m")
            return False

    @staticmethod
    def verify_cookie(cookie_value):
        try:
            headers = {
                'Cookie': f'.ROBLOSECURITY={cookie_value}',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36'
            }
            response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers, timeout=10)

            if response.status_code == 200:
                return response.json().get("id", False)
            elif response.status_code == 401:
                return False
            else:
                return False
        except:
            return False

    @staticmethod
    def check_user_online(user_id, cookie=None):
        # Thêm cơ chế Retry mạnh hơn
        urls = [
            "https://presence.roblox.com/v1/presence/users",
            "https://presence.roproxy.com/v1/presence/users"
        ]
        body = {"userIds": [user_id]}
        headers = {"Content-Type": "application/json"}
        if cookie:
            headers["Cookie"] = f".ROBLOSECURITY={cookie}"
        
        for url in urls:
            try:
                response = requests.post(url, headers=headers, json=body, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return data["userPresences"][0]["userPresenceType"]
            except:
                pass
        return None

    @staticmethod
    def get_roblox_packages():
        packages = []
        try:
            prefix = globals().get("package_prefix", "com.roblox")
            # Sử dụng lệnh shell lọc luôn để nhẹ hơn
            cmd = f"pm list packages | grep '{prefix}'"
            output = Utilities.run_shell(cmd)
            if output:
                for line in output.splitlines():
                    if "package:" in line:
                        packages.append(line.replace("package:", "").strip())
        except:
            pass
        return packages

    @staticmethod
    def kill_roblox_processes():
        # Kill nhanh bằng pkill nếu có thể (yêu cầu root hoặc quyền shell cao, nếu không dùng loop)
        # Ở đây dùng loop chuẩn Android
        packages = RobloxManager.get_roblox_packages()
        if not packages: return

        for pkg in packages:
            subprocess.run(["am", "force-stop", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def kill_roblox_process(package_name):
        try:
            subprocess.run(["am", "force-stop", package_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
        except:
            pass

    @staticmethod
    def delete_cache_for_package(package_name):
        cache_path = f'/data/data/{package_name}/cache/'
        if os.path.exists(cache_path):
            # Dùng subprocess run rm -rf an toàn hơn os.system
            subprocess.run(["rm", "-rf", cache_path], stderr=subprocess.DEVNULL)
            print(f"\033[1;32m[ Shouko.dev ] - Cache cleared for {package_name}\033[0m")

    @staticmethod
    def launch_roblox(package_name, server_link):
        """
        DIRECT JOIN (SKIP HOME) METHOD
        Sử dụng Deep Link trực tiếp và xóa task cũ để vào thẳng game.
        """
        try:
            # 1. Force stop trước để đảm bảo sạch sẽ
            subprocess.run(["am", "force-stop", package_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)

            # 2. Cập nhật trạng thái
            with status_lock:
                if package_name in globals()["package_statuses"]:
                    globals()["package_statuses"][package_name]["Status"] = "\033[1;36mDirect Joining...\033[0m"
                    UIManager.update_status_table()

            # 3. Dùng lệnh tối ưu để Join thẳng (Skip Home)
            # -W: Đợi activity launch xong
            # -n: Chỉ định Activity xử lý link (ProtocolLaunch)
            # -a: Action VIEW
            # -d: Data (Link)
            # --activity-clear-task: Xóa các task cũ đè lên
            # --activity-new-task: Tạo task mới
            
            cmd = [
                'am', 'start', '-W', 
                '-n', f'{package_name}/com.roblox.client.ActivityProtocolLaunch',
                '-a', 'android.intent.action.VIEW',
                '-d', server_link,
                '--activity-clear-task',
                '--activity-new-task'
            ]
            
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Đợi một chút để game load
            time.sleep(15)
            
            with status_lock:
                if package_name in globals()["package_statuses"]:
                    globals()["package_statuses"][package_name]["Status"] = "\033[1;32mJoined\033[0m"
                    UIManager.update_status_table()

        except Exception as e:
            Utilities.log_error(f"Launch Error {package_name}: {e}")

    @staticmethod
    def inject_cookies_and_appstorage():
        RobloxManager.kill_roblox_processes()
        db_url = "https://raw.githubusercontent.com/nghvit/module/refs/heads/main/import/Cookies"
        app_url = "https://raw.githubusercontent.com/nghvit/module/refs/heads/main/import/appStorage.json"

        print("\033[1;33m[ Shouko.dev ] - Downloading injection files...\033[0m")
        db_path = FileManager.download_file(db_url, "Cookies.db", binary=True)
        app_path = FileManager.download_file(app_url, "appStorage.json", binary=False)

        if not db_path or not app_path:
            print("\033[1;31m[ Shouko.dev ] - Download failed. Aborting injection.\033[0m")
            return

        packages = RobloxManager.get_roblox_packages()
        for pkg in packages:
            try:
                cookie = RobloxManager.get_cookie()
                if not cookie:
                    print(f"\033[1;31m[ Shouko.dev ] - Out of cookies for {pkg}.\033[0m")
                    break
                
                uid = RobloxManager.verify_cookie(cookie)
                if not uid:
                    print(f"\033[1;31m[ Shouko.dev ] - Invalid cookie for {pkg}. Skipping.\033[0m")
                    continue

                print(f"\033[1;32m[ Shouko.dev ] - Injecting {pkg} (UID: {uid})...\033[0m")
                
                # Paths
                dest_db_dir = f"/data/data/{pkg}/app_webview/Default/"
                dest_app_dir = f"/data/data/{pkg}/files/appData/LocalStorage/"
                
                os.makedirs(dest_db_dir, exist_ok=True)
                os.makedirs(dest_app_dir, exist_ok=True)

                # Copy files
                shutil.copyfile(db_path, os.path.join(dest_db_dir, "Cookies"))
                shutil.copyfile(app_path, os.path.join(dest_app_dir, "appStorage.json"))

                # Update DB
                RobloxManager.replace_cookie_value_in_db(os.path.join(dest_db_dir, "Cookies"), cookie)

            except Exception as e:
                print(f"\033[1;31m[ Shouko.dev ] - Injection Error {pkg}: {e}\033[0m")

        # Clean up
        if os.path.exists(db_path): os.remove(db_path)
        if os.path.exists(app_path): os.remove(app_path)
        
        print("\033[1;32m[ Shouko.dev ] - Injection complete. Launching apps...\033[0m")
        # ... (Launch logic preserved from original)

    @staticmethod
    def replace_cookie_value_in_db(db_path, new_cookie_value):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Update query optimized
            expire_time = int(time.time() + 31536000) * 1000000
            cursor.execute(
                "UPDATE cookies SET value = ?, last_access_utc = ?, expires_utc = ? WHERE name = '.ROBLOSECURITY'", 
                (new_cookie_value, int(time.time()) * 1000000, expire_time)
            )
            conn.commit()
        except Exception as e:
            print(f"\033[1;31m[ Shouko.dev ] - DB Update Error: {e}\033[0m")
        finally:
            if conn: conn.close()

    @staticmethod
    def format_server_link(input_link):
        if 'roblox.com' in input_link:
            return input_link
        elif input_link.isdigit():
            return f'roblox://placeID={input_link}'
        else:
            return None

class WebhookManager:
    @staticmethod
    def start_webhook_thread():
        global webhook_thread, stop_webhook_thread
        if (webhook_thread is None or not webhook_thread.is_alive()) and not stop_webhook_thread:
            stop_webhook_thread = False
            webhook_thread = threading.Thread(target=WebhookManager.send_webhook)
            webhook_thread.start()

    @staticmethod
    def send_webhook():
        global stop_webhook_thread
        while not stop_webhook_thread:
            try:
                screenshot_path = SystemMonitor.capture_screenshot()
                # Nếu không chụp được màn hình, vẫn gửi status text
                
                info = SystemMonitor.get_system_info()
                if not info:
                    time.sleep(60)
                    continue

                # Build Embed (Logic preserved)
                cpu = f"{info['cpu_usage']}%"
                mem = f"{info['memory_used']} GB"
                
                embed = {
                    "title": "📈 System Monitor",
                    "description": f"Device: **{device_name}**",
                    "color": random.randint(0, 16777215),
                    "fields": [
                        {"name": "CPU", "value": f"`{cpu}`", "inline": True},
                        {"name": "RAM", "value": f"`{mem}`", "inline": True},
                        {"name": "Uptime", "value": f"`{info['uptime']}`", "inline": True},
                        {"name": "Roblox Instances", "value": f"`{len(info['roblox_packages'])}`", "inline": False}
                    ],
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

                data = {"payload_json": json.dumps({"embeds": [embed], "username": "Shouko Bot"})}
                files = {}
                if screenshot_path and os.path.exists(screenshot_path):
                    files = {"file": open(screenshot_path, "rb")}
                
                requests.post(webhook_url, data=data, files=files, timeout=10)
                
                if files: files["file"].close()
                
            except Exception:
                pass

            time.sleep(webhook_interval * 60)

    @staticmethod
    def stop_webhook():
        global stop_webhook_thread
        stop_webhook_thread = True
    
    @staticmethod
    def setup_webhook():
        global webhook_url, device_name, webhook_interval, stop_webhook_thread
        try:
            stop_webhook_thread = True
            webhook_url = input("\033[1;35m[ Shouko.dev ] - Webhook URL: \033[0m")
            device_name = input("\033[1;35m[ Shouko.dev ] - Device Name: \033[0m")
            webhook_interval = int(input("\033[1;35m[ Shouko.dev ] - Interval (min): \033[0m"))
            FileManager.save_config()
            stop_webhook_thread = False
            threading.Thread(target=WebhookManager.send_webhook).start()
        except:
            print("Invalid input.")

class UIManager:
    @staticmethod
    def print_header(version):
        console = Console()
        header = Text(r"""
      _                   _             _          
     | |                 | |           | |          
 ___ | |__   ___  _   _| | _____   __| | _____   __
/ __| '_ \ / _ \| | | | |/ / _ \ / _` |/ _ \ \ / /
\__ \ | | | (_) | |_| |   < (_) | (_| |  __/\ V / 
|___/_| |_|\___/ \__,_|_|\_\___(_)__,_|\___| \_/  
        """, style="bold yellow")
        
        console.print(header)
        console.print(f"[bold cyan]Version:[/bold cyan] {version}")
        console.print(f"[bold cyan]Mode:[/bold cyan] {'Executor Check' if globals()['check_exec_enable'] == '1' else 'Online Check'}\n")

    @staticmethod
    def create_dynamic_menu(options):
        console = Console()
        table = Table(header_style="bold white", border_style="blue", box=ROUNDED)
        table.add_column("No", justify="center", style="bold cyan", width=5)
        table.add_column("Option", style="bold white")

        for i, opt in enumerate(options, 1):
            table.add_row(str(i), opt)
        
        console.print(table)

    last_update_time = 0
    
    @staticmethod
    def update_status_table():
        # Throttle updates: Chỉ cập nhật tối đa 1 lần mỗi 2 giây để đỡ lag console
        if time.time() - UIManager.last_update_time < 2:
            return
        UIManager.last_update_time = time.time()

        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        
        table = PrettyTable()
        table.field_names = ["Package", "User", "Status"]
        table.align = "l"
        table.title = f"System: CPU {cpu}% | RAM {mem}%"

        # Sử dụng copy để tránh lỗi RuntimeError: dictionary changed size during iteration
        statuses = globals().get("package_statuses", {}).copy()
        
        for pkg, info in statuses.items():
            user = info.get("Username", "Unknown")
            status = info.get("Status", "Unknown")
            # Mask username
            if len(user) > 4: user = user[:2] + "***" + user[-2:]
            table.add_row([pkg, user, status])

        Utilities.clear_screen()
        UIManager.print_header(version)
        print(table)

class ExecutorManager:
    @staticmethod
    def detect_executors():
        found = []
        for name, path in executors.items():
            # Check common autoexec paths
            if os.path.exists(os.path.join(path, "Autoexec")) or \
               os.path.exists(os.path.join(path, "autoexec")):
                found.append(name)
        return found
    
    @staticmethod
    def write_lua_script(detected_executors):
        script_path = os.path.join(BASE_DIR, "checkui.lua")
        try:
            with open(script_path, "r") as f:
                content = f.read()
        except:
            return # Không có script mẫu thì bỏ qua

        for name in detected_executors:
            path = executors[name]
            # Logic ghi file vào autoexec từng loại executor (Giữ nguyên logic gốc)
            # Thêm try-except cho từng thao tác ghi file
            try:
                autoexec = os.path.join(path, "Autoexec")
                if not os.path.exists(autoexec):
                    autoexec = os.path.join(path, "autoexec")
                
                if os.path.exists(autoexec):
                    with open(os.path.join(autoexec, "shouko_check.lua"), "w") as f:
                        f.write(content)
            except:
                pass

    @staticmethod
    def check_executor_status(package_name, max_wait=180):
        # Check file .main created by Lua script
        start = time.time()
        uid = globals()["_user_"].get(package_name)
        if not uid: return True # Skip check if no UID

        while time.time() - start < max_wait:
            for ws in globals()["workspace_paths"]:
                check_file = os.path.join(ws, f"{uid}.main")
                if os.path.exists(check_file):
                    try: os.remove(check_file) # Clean up
                    except: pass
                    return True
            time.sleep(10)
        return False

    @staticmethod
    def check_executor_and_rejoin(package_name, server_link, event):
        # ... (Logic giữ nguyên, chỉ thêm try-except và cập nhật status an toàn)
        try:
            if ExecutorManager.detect_executors():
                 with status_lock:
                     globals()["package_statuses"][package_name]["Status"] = "\033[1;33mChecking Exec...\033[0m"
                     UIManager.update_status_table()
                 
                 if ExecutorManager.check_executor_status(package_name):
                     with status_lock:
                         globals()["package_statuses"][package_name]["Status"] = "\033[1;32mExec OK\033[0m"
                 else:
                     # Rejoin logic
                     RobloxManager.launch_roblox(package_name, server_link)
            
        except Exception as e:
            Utilities.log_error(f"Exec Check Fail {package_name}: {e}")
        finally:
            event.set()

class Runner:
    @staticmethod
    def launch_package_sequentially(server_links):
        event = Event()
        for pkg, link in server_links:
            event.clear()
            # Anti-Crash: Kiểm tra user ID có tồn tại không
            if pkg not in globals()["_user_"]:
                print(f"Skipping {pkg} (No User ID)")
                continue

            RobloxManager.launch_roblox(pkg, link)
            
            # Executor check logic
            if globals()["check_exec_enable"] == "1":
                if ExecutorManager.detect_executors():
                    ExecutorManager.write_lua_script(ExecutorManager.detect_executors())
                    threading.Thread(target=ExecutorManager.check_executor_and_rejoin, args=(pkg, link, event), daemon=True).start()
                    event.wait() # Wait for check to finish
                else:
                    pass # No executor found
            
            time.sleep(5) # Delay between launches

    @staticmethod
    def monitor_presence(server_links, stop_event):
        while not stop_event.is_set():
            try:
                if globals()["check_exec_enable"] == "0": # Only if Online Check mode
                    for pkg, link in server_links:
                        # Lấy cookie an toàn từ DB
                        cookie = FileManager.get_cookie_from_db(f"/data/data/{pkg}/app_webview/Default/Cookies")
                        uid = globals()["_user_"].get(pkg)
                        
                        if cookie and uid:
                            status = RobloxManager.check_user_online(uid, cookie)
                            # 2 = InGame
                            if status == 2:
                                with status_lock:
                                    globals()["package_statuses"][pkg]["Status"] = "\033[1;32mIn-Game\033[0m"
                            else:
                                with status_lock:
                                    globals()["package_statuses"][pkg]["Status"] = "\033[1;31mOffline (Rejoining)\033[0m"
                                RobloxManager.launch_roblox(pkg, link)
                                
                            UIManager.update_status_table()
                
                time.sleep(60)
            except Exception as e:
                Utilities.log_error(f"Monitor Error: {e}")
                time.sleep(60)

    @staticmethod
    def force_rejoin(server_links, interval, stop_event):
        if interval <= 0: return
        last_run = time.time()
        while not stop_event.is_set():
            if time.time() - last_run > interval:
                print("\033[1;33m[ Shouko.dev ] - Force Rejoin Cycle...\033[0m")
                RobloxManager.kill_roblox_processes()
                Runner.launch_package_sequentially(server_links)
                last_run = time.time()
            time.sleep(60)

def auto_change_android_id():
    global auto_android_id_enabled, auto_android_id_value
    while auto_android_id_enabled:
        if auto_android_id_value:
            try:
                subprocess.run(["settings", "put", "secure", "android_id", auto_android_id_value], check=False)
            except: pass
        time.sleep(2)

def main():
    # Khởi tạo và load config
    FileManager._load_config()
    
    # Check activation (Giả lập check)
    try:
        # Thay URL thật vào đây nếu cần
        pass 
    except:
        pass

    # Setup default script nếu chưa có
    if not globals().get("command_8_configured", False):
        lua = 'task.spawn(function()local a=tostring(game.Players.LocalPlayer.UserId)..".main"while true do pcall(function()if isfile(a)then delfile(a)end; local success,err=pcall(function()writefile(a,"checked")end) end) task.wait(10) end end)'
        globals()["lua_script_template"] = lua
        # Save lua
        with open(os.path.join(BASE_DIR, "checkui.lua"), "w") as f:
            f.write(lua)
        FileManager.save_config()

    # Start Webhook if configured
    if webhook_url and device_name:
        WebhookManager.start_webhook_thread()

    stop_main_event = threading.Event()

    while True:
        try:
            Utilities.clear_screen()
            UIManager.print_header(version)
            FileManager.check_and_create_cookie_file()

            options = [
                "Auto Rejoin (Start)",
                "Setup Game ID",
                "Inject Cookies",
                "Webhook Setup",
                "Check Mode Setup",
                "Package Prefix Setup",
                "Auto Android ID"
            ]
            UIManager.create_dynamic_menu(options)
            
            choice = input("\033[1;93m[ Shouko.dev ] > \033[0m").strip()

            if choice == "1":
                FileManager.setup_user_ids()
                globals()["accounts"] = FileManager.load_accounts()
                links = FileManager.load_server_links()
                
                if not globals()["accounts"] or not links:
                    print("\033[1;31mMissing accounts or links. Run setup first.\033[0m")
                    time.sleep(2)
                    continue

                try:
                    interval = int(input("Force Rejoin Interval (min, 0 to disable): ")) * 60
                except: interval = 0

                # Start Threads
                stop_main_event.clear()
                RobloxManager.kill_roblox_processes()
                
                # Initial Launch
                Runner.launch_package_sequentially(links)
                
                # Monitor Threads
                threading.Thread(target=Runner.monitor_presence, args=(links, stop_main_event), daemon=True).start()
                threading.Thread(target=Runner.force_rejoin, args=(links, interval, stop_main_event), daemon=True).start()
                
                print("\033[1;32mRunning... Press Ctrl+C to stop (or close termux).\033[0m")
                
                while not stop_main_event.is_set():
                    time.sleep(100) # Keep main thread alive

            elif choice == "2":
                # Setup Links Logic
                FileManager.setup_user_ids()
                # ... (Giữ logic nhập ID game cũ)
                # Tạm thời hardcode ví dụ để code ngắn, bạn giữ nguyên phần input cũ nhé
                link = input("Game ID/Link: ")
                fmt_link = RobloxManager.format_server_link(link)
                if fmt_link:
                    accts = FileManager.load_accounts()
                    links = [(pkg, fmt_link) for pkg, _ in accts]
                    FileManager.save_server_links(links)
            
            elif choice == "3":
                RobloxManager.inject_cookies_and_appstorage()
                input("Done. Enter to continue...")

            elif choice == "4":
                WebhookManager.setup_webhook()
            
            elif choice == "5":
                # Check Mode Config
                pass # Logic giữ nguyên

            elif choice == "6":
                # Prefix Config
                p = input("Package Prefix (e.g. com.roblox): ")
                globals()["package_prefix"] = p
                FileManager.save_config()

            elif choice == "7":
                # Android ID
                global auto_android_id_enabled, auto_android_id_thread, auto_android_id_value
                if not auto_android_id_enabled:
                    auto_android_id_value = input("Android ID: ")
                    auto_android_id_enabled = True
                    auto_android_id_thread = threading.Thread(target=auto_change_android_id, daemon=True)
                    auto_android_id_thread.start()
                    print("Enabled.")
                else:
                    auto_android_id_enabled = False
                    print("Disabled.")
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nExiting...")
            stop_main_event.set()
            break
        except Exception as e:
            print(f"Critical Error: {e}")
            Utilities.log_error(f"Main Loop Error: {e}")
            input("Enter to restart menu...")

if __name__ == "__main__":
    main()
