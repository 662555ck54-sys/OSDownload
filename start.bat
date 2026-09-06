@echo off
setlocal

where py >nul 2>nul
if %errorlevel%==0 (
  py "%~dp0app\main.py" %*
  exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%~dp0app\main.py" %*
  exit /b %errorlevel%
)

echo Python 3.10+ is required.
echo Download it from: https://www.python.org/downloads/
echo Then run start.bat again.
pause