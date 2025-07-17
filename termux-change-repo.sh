#!/data/data/com.termux/files/usr/bin/bash

source /data/data/com.termux/files/usr/bin/termux-setup-package-manager || exit 1

ETC="/data/data/com.termux/files/usr/etc/termux"
CHOSEN="$ETC/chosen_mirrors"
MIRROR="$ETC/mirrors/all"

command -v apt >/dev/null || exit 1

[[ "$TERMUX_APP_PACKAGE_MANAGER" == "pacman" ]] && {
  read -p "Chỉ dùng cho apt. Tiếp tục? [y/N] " -n1 r; echo
  [[ ! "$r" =~ ^[Yy]$ ]] && exit
}

rm -f "$CHOSEN" && ln -s "$MIRROR" "$CHOSEN"

TERMUX_APP_PACKAGE_MANAGER=apt pkg --check-mirror update
