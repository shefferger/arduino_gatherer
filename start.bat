@echo off
(echo.set sh=CreateObject^("Wscript.shell"^)
echo.sh.Run """%-nx0"" 1", 0)>launch.vbs
if "%-1"=="" (start "" "launch.vbs"&exit /b)
start "" python form.py
