@echo off
setlocal

set "ProgramName=python.exe"

tasklist | find /i "%ProgramName%" > nul

if %errorlevel% equ 0 (
    echo %ProgramName% is running.

) else (
	
	echo VPN Notifier Window
	echo In Progress .....
	python vpn.py
	pause
)


endlocal