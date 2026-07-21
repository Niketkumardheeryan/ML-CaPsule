# run_app.ps1
# Activates the virtual environment and launches the Streamlit app on port 8501.
param(
    [string]$VenvDir = ".venv",
    [int]$Port = 8501
)

$activate = "${VenvDir}\Scripts\Activate.ps1"
if (-Not (Test-Path $activate)) {
    Write-Error "Activation script not found. Have you run setup_env.ps1?"
    exit 1
}

Write-Host "Starting Streamlit on port $Port..."
& powershell -NoProfile -ExecutionPolicy Bypass -Command "& '${activate}'; streamlit run app.py --server.port $Port"
