@echo off

powershell Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
powershell -File %~dp0main_script.ps1

pause