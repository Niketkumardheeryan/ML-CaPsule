# setup_env.ps1
# Creates a virtual environment, installs dependencies, and downloads spaCy model.
# Run from project root in PowerShell (not as administrator):
#   .\setup_env.ps1

param(
    [string]$Python = "python",
    [string]$VenvDir = ".venv"
)

Write-Host "Using Python:" $Python

if (-Not (Test-Path ".\requirements.txt")) {
    Write-Error "requirements.txt not found in current folder. Run this script from the project root."
    exit 1
}

# Create virtualenv if missing
if (-Not (Test-Path $VenvDir)) {
    & $Python -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment with $Python"
        exit 1
    }
    Write-Host "Virtual environment created at" $VenvDir
} else {
    Write-Host "Virtual environment already exists at" $VenvDir
}

# Activate and install
$activate = "${VenvDir}\Scripts\Activate.ps1"
if (-Not (Test-Path $activate)) {
    Write-Error "Activation script not found: $activate"
    exit 1
}

Write-Host "Installing dependencies into virtualenv..."
& powershell -NoProfile -ExecutionPolicy Bypass -Command "& '${activate}'; python -m pip install --upgrade pip; pip install -r requirements.txt"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install Python packages. Check the error above."
    exit 1
}

Write-Host "Downloading spaCy model en_core_web_sm..."
& powershell -NoProfile -ExecutionPolicy Bypass -Command "& '${activate}'; python -m spacy download en_core_web_sm"

Write-Host "Setup complete. To run the app, activate the venv and run:"
Write-Host "  .\\.venv\\Scripts\\Activate.ps1"
Write-Host "  streamlit run app.py"
