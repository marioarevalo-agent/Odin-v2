# ══════════════════════════════════════════════════════════════════════════
#  ONYX GCP DEPLOYMENT HELPER SCRIPT
#  Automates Cloud Build & Cloud Run deployment for project: proy-anla-poc
# ══════════════════════════════════════════════════════════════════════════

$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "            ONYX SERVICES GCP DEPLOYMENT                 " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# 1. Check gcloud CLI
Write-Host "[1/4] Verificando instalación de Google Cloud CLI..." -ForegroundColor Yellow
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Error "Google Cloud CLI (gcloud) no está instalado o no se encuentra en el PATH."
    Write-Host "Por favor, instálalo desde: https://cloud.google.com/sdk/docs/install" -ForegroundColor Red
    exit 1
}
Write-Host "✔ Google Cloud CLI detectado." -ForegroundColor Green

# 2. Check active account and set project
Write-Host "[2/4] Configurando proyecto activo a 'proy-anla-poc'..." -ForegroundColor Yellow
try {
    # Check if user is logged in
    $activeAccount = gcloud config get-value account 2>$null
    if ([string]::IsNullOrEmpty($activeAccount)) {
        Write-Host "No hay ninguna cuenta autenticada en gcloud. Iniciando flujo de login..." -ForegroundColor Cyan
        gcloud auth login
        $activeAccount = gcloud config get-value account
    }
    Write-Host "✔ Autenticado como: $activeAccount" -ForegroundColor Green

    # Set project
    gcloud config set project proy-anla-poc
    Write-Host "✔ Proyecto de GCP configurado a 'proy-anla-poc'." -ForegroundColor Green
} catch {
    Write-Error "Error configurando el proyecto o cuenta en gcloud: $_"
    exit 1
}

# 3. Cloud Build Submission
Write-Host "[3/4] Enviando código a Google Cloud Build..." -ForegroundColor Yellow
Write-Host "Esto compilará la imagen Docker en la nube y la registrará en GCR." -ForegroundColor Gray
try {
    gcloud builds submit --tag gcr.io/proy-anla-poc/onyx-server
    Write-Host "✔ Imagen compilada con éxito: gcr.io/proy-anla-poc/onyx-server" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en Google Cloud Build." -ForegroundColor Red
    Write-Host "Asegúrate de que tu cuenta ($activeAccount) tiene permisos de 'Cloud Build Editor' y 'Storage Admin' en el proyecto 'proy-anla-poc'." -ForegroundColor Yellow
    exit 1
}

# 4. Cloud Run Deploy
Write-Host "[4/4] Desplegando en Google Cloud Run..." -ForegroundColor Yellow
try {
    gcloud run deploy onyx-server `
        --image gcr.io/proy-anla-poc/onyx-server `
        --platform managed `
        --region us-central1 `
        --allow-unauthenticated

    $serviceUrl = gcloud run services describe onyx-server --platform managed --region us-central1 --format="value(status.url)" 2>$null
    
    Write-Host ""
    Write-Host "=========================================================" -ForegroundColor Green
    Write-Host " 🎉 ¡DESPLIEGUE COMPLETADO CON ÉXITO!                     " -ForegroundColor Green
    Write-Host "=========================================================" -ForegroundColor Green
    Write-Host "Servicio: onyx-server" -ForegroundColor Green
    Write-Host "URL Pública: $serviceUrl" -ForegroundColor Green
    Write-Host "=========================================================" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al desplegar en Cloud Run." -ForegroundColor Red
    Write-Host "Asegúrate de que tu cuenta ($activeAccount) tiene permisos de 'Cloud Run Admin' y 'Service Account User' en el proyecto 'proy-anla-poc'." -ForegroundColor Yellow
    exit 1
}
