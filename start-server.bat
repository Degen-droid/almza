@echo off
echo Starting Almaza Web Server...
echo.
echo Your website will be available at:
echo PC: http://127.0.0.1:8000/almaza-perfect-layout.html
echo Phone: http://192.168.0.105:8000/almaza-perfect-layout.html
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "C:\Users\davis\Desktop\Almaza"
python -m http.server 8000
pause



















