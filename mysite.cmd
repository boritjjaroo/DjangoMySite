@echo off
rem powershell.exe -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned"
rem PowerShell.exe -Command "& '% ~ dpn0.ps1'"
rem 프로젝트 경로
cd "C:\Users\~~~~~\source\python\projects\mysite"
set DJANGO_SETTINGS_MODULE=config.settings.local
rem 패키지 추가 경로
set PYTHONPATH=C:\Users\~~~~~\source\python\mypackages

rem django 키 설정 (특수문자 escape 처리 필요)
rem % -> %%,  ^ -> ^^,  & -> ^&
set "DJANGO_SECRET_KEY=~~~~~"
set DJANGO_ALLOWED_HOSTS=
rem DB 접속 설정
set "DJANGO_DB_ENGINE=~~~~~"
set "DJANGO_DB_NAME=~~~~~"
set "DJANGO_DB_USER=~~~~~"
set "DJANGO_DB_PASSWORD=~~~~~"
set "DJANGO_DB_HOST=~~~~~"
set "DJANGO_DB_PORT=~~~~~"

C:\Users\~~~~~\source\python\venvs\mysite\Scripts\activate
