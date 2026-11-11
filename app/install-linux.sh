#!/usr/bin/env bash
# Adds the handbook to the application menu and the desktop. Run again after moving the folder.
set -e
DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
chmod +x "$DIR/start-linux.sh"
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPS"
ENTRY="$APPS/bioinformatics.desktop"
cat > "$ENTRY" <<DESK
[Desktop Entry]
Type=Application
Name=بیوانفورماتیک
Name[en]=Bioinformatics
Comment=درس‌نامهٔ تعاملی باکتری‌شناسی تشخیصی
Exec="$DIR/start-linux.sh"
Icon=$DIR/assets/icon/icon-512.png
Terminal=false
Categories=Education;MedicalSoftware;
StartupWMClass=Bioinformatics
DESK
chmod +x "$ENTRY"
DESKTOP="$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")"
if [ -d "$DESKTOP" ]; then
  cp "$ENTRY" "$DESKTOP/bioinformatics.desktop"
  chmod +x "$DESKTOP/bioinformatics.desktop"
  gio set "$DESKTOP/bioinformatics.desktop" metadata::trusted true 2>/dev/null || true
fi
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" 2>/dev/null || true
echo "Installed: application menu and desktop icon ($DESKTOP)."
