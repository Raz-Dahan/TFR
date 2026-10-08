import psutil
import pystray
from PIL import Image, ImageDraw, ImageFont
import time
import threading
import subprocess
import sys


# =========================
# Global settings
# =========================

running = True
text_color = (255, 255, 255)  # White by default


# =========================
# Make left-click open menu on Windows
# =========================

def patch_pystray_left_click_menu():
    if sys.platform != "win32":
        return

    try:
        import pystray._win32

        WM_LBUTTONUP = 0x0202
        WM_RBUTTONUP = 0x0205

        original_on_notify = pystray._win32.Icon._on_notify

        def patched_on_notify(self, wparam, lparam):
            if lparam == WM_LBUTTONUP:
                return original_on_notify(self, wparam, WM_RBUTTONUP)

            return original_on_notify(self, wparam, lparam)

        pystray._win32.Icon._on_notify = patched_on_notify

    except Exception:
        pass


patch_pystray_left_click_menu()


# =========================
# RAM monitor
# =========================

def get_memory_usage():
    return psutil.virtual_memory().percent


# =========================
# Exit program
# =========================

def exit_program(icon, _item):
    global running
    running = False
    icon.stop()


# =========================
# Toggle text color
# =========================

def toggle_text_color(icon, _item):
    global text_color

    if text_color == (255, 255, 255):
        text_color = (0, 0, 0)  # Black
    else:
        text_color = (255, 255, 255)  # White



# =========================
# Open WinMemoryCleaner
# =========================

def open_win_memory_cleaner(icon, _item):
    app_path = r"C:\Users\razda\WinMemoryCleaner.exe"

    try:
        subprocess.Popen([app_path])
    except OSError as e:
        print(f"Could not launch WinMemoryCleaner: {e}")


# =========================
# Toggle Windows display scale
# =========================

def toggle_display_scale(icon, _item):
    threading.Thread(target=run_display_scale_toggle, daemon=True).start()


def run_display_scale_toggle():
    ps_command = r"""
Import-Module DisplayConfig -ErrorAction Stop

$CurrentScale = Get-DisplayScale -DisplayId 1

if ($CurrentScale.CurrentScale -eq 175) {
    Set-DisplayScale -DisplayId 1 -Scale 225
}
elseif ($CurrentScale.CurrentScale -eq 225) {
    Set-DisplayScale -DisplayId 1 -Scale 175
}
"""

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0

    subprocess.run(
        [
            "powershell.exe",
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-WindowStyle",
            "Hidden",
            "-Command",
            ps_command
        ],
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


# =========================
# Create tray icon image
# =========================

def create_icon(usage_percentage):
    icon_size = 100

    image = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    font_size = int(0.75 * icon_size)

    try:
        font = ImageFont.truetype("segoeui.ttf", font_size)
    except:
        font = ImageFont.load_default()

    usage_text = f"{usage_percentage:.0f}"

    bbox = draw.textbbox((0, 0), usage_text, font=font)
    usage_width = bbox[2] - bbox[0]
    usage_height = bbox[3] - bbox[1]

    icon_center_x = icon_size / 2
    icon_center_y = icon_size / 2

    usage_x = icon_center_x - usage_width / 2
    usage_y = icon_center_y - int(usage_height / 1.05)

    draw.text(
        (usage_x, usage_y),
        usage_text,
        font=font,
        fill=text_color
    )

    return image


# =========================
# Update tray icon
# =========================

def update_icon_thread(icon):
    while running:
        memory_percentage = get_memory_usage()

        icon.title = f"RAM Usage: {memory_percentage:.0f}%"
        icon.icon = create_icon(memory_percentage)

        time.sleep(0.5)


# =========================
# Create taskbar icon
# =========================

def create_taskbar_icon():
    memory_percentage = get_memory_usage()

    menu = (
        pystray.MenuItem("Toggle Text Color", toggle_text_color),
        pystray.MenuItem("Toggle Display Scale", toggle_display_scale),
        pystray.MenuItem("Exit", exit_program)
    )

    icon = pystray.Icon(
        "RAM Display",
        create_icon(memory_percentage),
        "RAM Display",
        menu
    )

    update_thread = threading.Thread(
        target=update_icon_thread,
        args=[icon],
        daemon=True
    )

    update_thread.start()
    icon.run()


if __name__ == "__main__":
    create_taskbar_icon()