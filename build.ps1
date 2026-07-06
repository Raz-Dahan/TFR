pip install pyinstaller

python -m PyInstaller --onefile --noconsole --icon=logo.ico TFR.py

Write-Host ""
Write-Host "Build complete."
Write-Host "The .exe file is inside the dist folder."