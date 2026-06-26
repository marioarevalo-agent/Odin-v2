@echo off
title ONYX GCP Deployment Helper
cls
echo =========================================================
echo             ONYX SERVICES GCP DEPLOYMENT
echo =========================================================
echo.
echo Iniciando script de despliegue en PowerShell...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy_gcp.ps1"
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] El despliegue ha fallado. Por favor, revisa los mensajes anteriores.
    pause
    exit /b %errorlevel%
)
echo.
echo [INFO] Despliegue finalizado exitosamente.
pause
