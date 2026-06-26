# ==========================================================================
#  ONYX BIGQUERY INITIALIZATION SCRIPT
#  Creates dataset and tables in GCP project: proy-anla-poc
# ==========================================================================

$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "         ONYX BIGQUERY SCHEMA INITIALIZATION            " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$PROJECT_ID = "proy-anla-poc"
$DATASET_ID = "onyx"
$LOCATION = "us-central1"

# 1. Create Dataset
Write-Host "[1/7] Creando dataset '$DATASET_ID' en la ubicacion '$LOCATION'..." -ForegroundColor Yellow
try {
    # Check if dataset already exists
    $datasets = bq ls --project_id=$PROJECT_ID --format=json | ConvertFrom-Json
    $exists = $false
    foreach ($ds in $datasets) {
        if ($ds.datasetReference.datasetId -eq $DATASET_ID) {
            $exists = $true
            break
        }
    }
    if ($exists) {
        Write-Host "[OK] El dataset '$DATASET_ID' ya existe." -ForegroundColor Green
    } else {
        bq mk --dataset --project_id=$PROJECT_ID --location=$LOCATION $DATASET_ID
        Write-Host "[OK] Dataset '$DATASET_ID' creado con exito." -ForegroundColor Green
    }
} catch {
    # Fallback to mk directly in case ls format differs
    try {
        bq mk --dataset --project_id=$PROJECT_ID --location=$LOCATION $DATASET_ID
        Write-Host "[OK] Dataset '$DATASET_ID' creado." -ForegroundColor Green
    } catch {
        Write-Host "El dataset ya existe o hubo un error al crearlo: $_" -ForegroundColor Gray
    }
}

# Helper to create table with schema
function Create-BQTable {
    param(
        [string]$TableName,
        [string]$SchemaDefinition
    )
    Write-Host "Creando tabla '$TableName'..." -ForegroundColor Yellow
    try {
        $fullTableId = "${PROJECT_ID}:${DATASET_ID}.${TableName}"
        $null = bq show --project_id=$PROJECT_ID "${DATASET_ID}.${TableName}" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] La tabla '$TableName' ya existe." -ForegroundColor Green
        } else {
            bq mk --table --project_id=$PROJECT_ID $fullTableId $SchemaDefinition
            Write-Host "[OK] Tabla '$TableName' creada exitosamente." -ForegroundColor Green
        }
    } catch {
        Write-Host "La tabla '$TableName' ya existe o hubo un error: $_" -ForegroundColor Gray
    }
}

# 2. Table: eq_users
$usersSchema = "user_id:STRING,email:STRING,password_hash:STRING,salt:STRING,full_name:STRING,role:STRING,avatar:STRING,created_at:STRING,last_login:STRING,is_active:BOOLEAN"
Create-BQTable -TableName "eq_users" -SchemaDefinition $usersSchema

# 3. Table: eq_sync_status
$syncSchema = "device_id:STRING,last_ip:STRING,status:STRING,last_sync:STRING,timestamp:STRING"
Create-BQTable -TableName "eq_sync_status" -SchemaDefinition $syncSchema

# 4. Table: eq_hardware_metrics
$metricsSchema = "timestamp:STRING,device_id:STRING,cpu_usage:FLOAT,ram_usage:FLOAT,disk_free_gb:FLOAT,network_latency_ms:FLOAT,cause_root:STRING,cause_process:STRING,device_type:STRING,battery_percent:INTEGER,battery_status:STRING,top_processes:STRING,browser_history:STRING,network_info:STRING,usb_ports:STRING,event_logs:STRING"
Create-BQTable -TableName "eq_hardware_metrics" -SchemaDefinition $metricsSchema

# 5. Table: eq_security_events
$securitySchema = "timestamp:STRING,device_id:STRING,event_type:STRING,details:STRING,severity:STRING"
Create-BQTable -TableName "eq_security_events" -SchemaDefinition $securitySchema

# 6. Table: eq_kpi_definitions
$kpiSchema = "kpi_id:STRING,kpi_name:STRING,formula:STRING,target_value:FLOAT,created_by:STRING,created_at:STRING"
Create-BQTable -TableName "eq_kpi_definitions" -SchemaDefinition $kpiSchema

# 7. Table: eq_whatsapp_interactions
$waSchema = "timestamp:STRING,phone_number:STRING,user_query:STRING,bot_response:STRING,intent_detected:STRING,tokens_used:INTEGER"
Create-BQTable -TableName "eq_whatsapp_interactions" -SchemaDefinition $waSchema

Write-Host "=========================================================" -ForegroundColor Green
Write-Host " 🎉 INICIALIZACION DE BIGQUERY COMPLETADA CON EXITO!      " -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
