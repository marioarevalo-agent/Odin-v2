# ==========================================================================
#  ONYX GCP DEPLOYMENT HELPER SCRIPT
#  Automates Cloud Build & Cloud Run deployment for project: proy-anla-poc
# ==========================================================================

$ErrorActionPreference = "Stop"

Write-Host "========================================================="
Write-Host "            ONYX SERVICES GCP DEPLOYMENT                 "
Write-Host "========================================================="

# 1. Check gcloud CLI
Write-Host "[1/4] Verificando instalacion de Google Cloud CLI..."
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Error "Google Cloud CLI (gcloud) no esta instalado o no se encuentra en el PATH."
    Write-Host "Por favor, instalalo desde: https://cloud.google.com/sdk/docs/install"
    exit 1
}
Write-Host "[OK] Google Cloud CLI detectado."

# 2. Check active account and set project
Write-Host "[2/4] Configurando proyecto activo a 'proy-anla-poc'..."
try {
    # Check if user is logged in
    $activeAccount = gcloud config get-value account 2>$null
    if ([string]::IsNullOrEmpty($activeAccount)) {
        Write-Host "No hay ninguna cuenta autenticada en gcloud. Iniciando flujo de login..."
        gcloud auth login
        $activeAccount = gcloud config get-value account
    }
    Write-Host "[OK] Autenticado como: $activeAccount"

    # Set project
    gcloud config set project proy-anla-poc
    Write-Host "[OK] Proyecto de GCP configurado a 'proy-anla-poc'."
} catch {
    Write-Error "Error configurando el proyecto o cuenta en gcloud: $_"
    exit 1
}

# 3. Cloud Build Submission
Write-Host "[3/4] Enviando codigo a Google Cloud Build..."
Write-Host "Esto compilara la imagen Docker en la nube y la registrara en GCR."
try {
    gcloud builds submit --tag gcr.io/proy-anla-poc/onyx-server
    Write-Host "[OK] Imagen compilada con exito: gcr.io/proy-anla-poc/onyx-server"
} catch {
    Write-Host "[ERROR] Error en Google Cloud Build."
    Write-Host "Asegurate de que tu cuenta ($activeAccount) tiene permisos de 'Cloud Build Editor' y 'Storage Admin' en el proyecto 'proy-anla-poc'."
    exit 1
}

# 4. Cloud Run Deploy
Write-Host "[4/4] Desplegando en Google Cloud Run..."
try {
    gcloud run deploy onyx-server `
        --image gcr.io/proy-anla-poc/onyx-server `
        --platform managed `
        --region us-central1 `
        --allow-unauthenticated

    $serviceUrl = gcloud run services describe onyx-server --platform managed --region us-central1 --format="value(status.url)" 2>$null
    
    Write-Host ""
    Write-Host "========================================================="
    Write-Host "  DESPLIEGUE COMPLETADO CON EXITO!                       "
    Write-Host "========================================================="
    Write-Host "Servicio: onyx-server"
    Write-Host "URL Publica: $serviceUrl"
    Write-Host "========================================================="
} catch {
    Write-Host "[ERROR] Error al desplegar en Cloud Run."
    Write-Host "Asegurate de que tu cuenta ($activeAccount) tiene permisos de 'Cloud Run Admin' y 'Service Account User' en el proyecto 'proy-anla-poc'."
    exit 1
}
