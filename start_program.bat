@echo off

powershell Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
powershell -File ./start_program.ps1

pause