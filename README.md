# TFR - Tools for Raz

**TFR** is a small Windows taskbar utility built in Python.

The app currently includes:

- A RAM monitor shown directly in the Windows taskbar tray icon
- A right-click menu option to toggle the icon text color
- A right-click menu option to toggle Windows display scale
- A simple Exit option to close the app

The project runs on **Windows only**.

You can download the latest [Release](https://github.com/Raz-Dahan/TFR/releases/latest) and follow the installation instructions.
Once opened, TFR will keep running in the background until you right-click the tray icon and choose **Exit**.

---

## Features

### RAM Monitor

TFR displays the current RAM usage percentage directly in the taskbar tray icon.

### Toggle Text Color

Right-click the tray icon and select:

```text
Toggle Text Color
```

This switches the icon text between white and black.

### Toggle Display Scale

Right-click the tray icon and select:

```text
Toggle Display Scale
```

This toggles the Windows display scale between:

```text
175% <-> 225%
```

This feature uses PowerShell through Python and requires the `DisplayConfig` PowerShell module to be installed once on the computer.

---

## Requirements

- Windows
- Python 3.6 or higher
- `DisplayConfig` PowerShell module, for the display scale toggle feature

Python packages:

```txt
psutil
pystray
Pillow
```

PowerShell module:

```powershell
Install-Module DisplayConfig -Scope CurrentUser
```

> `requirements.txt` is only for Python packages. The `DisplayConfig` module is installed separately through PowerShell.

---

## Installation

1. Clone this repository or download the source code.

```powershell
git clone https://github.com/Raz-Dahan/MemoryDisplay.git
cd MemoryDisplay
```

2. Create a virtual environment, optional but recommended:

```powershell
python -m venv venv
```

3. Activate the virtual environment:

```powershell
venv\Scripts\activate
```

4. Install the required Python packages from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

5. Install the PowerShell module required for the display scale toggle:

```powershell
Install-Module DisplayConfig -Scope CurrentUser
```

If PowerShell asks for permission to install from PSGallery, type:

```powershell
Y
```

---

## Usage

Run the app:

```powershell
python ram_monitor.py
```

The taskbar tray icon will show the current RAM usage percentage.

To open the menu, right-click the tray icon.

Available menu options:

```text
Toggle Text Color
Toggle Display Scale
Exit
```

To close the app, right-click the tray icon and select:

```text
Exit
```

---

## Build as an EXE

To use TFR as a standalone Windows program, install PyInstaller:

```powershell
pip install pyinstaller
```

Then build the app:

```powershell
pyinstaller.exe --onefile --noconsole --icon=logo.ico ram_monitor.py
```

After the build is complete, the `.exe` file will be inside the `dist` folder.

---

## Optional Setup Script

If you want one setup file that installs both the Python packages and the PowerShell module, create a file named `setup.ps1`:

```powershell
pip install -r requirements.txt
Install-Module DisplayConfig -Scope CurrentUser
```

Then run it from PowerShell:

```powershell
.\setup.ps1
```

---

## Customization

You can customize the tray icon appearance by editing the `create_icon()` function in `ram_monitor.py`.

For example, you can change:

- Icon size
- Font
- Text color
- Text position
- Refresh rate

You can also edit the display scale values inside the `toggle_display_scale()` function.

Default scale toggle:

```text
175% <-> 225%
```

---

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- The taskbar icon is implemented using the [pystray](https://github.com/moses-palmer/pystray) library.
- RAM usage is read using the [psutil](https://github.com/giampaolo/psutil) library.
- Icon text rendering is handled with [Pillow](https://github.com/python-pillow/Pillow).
