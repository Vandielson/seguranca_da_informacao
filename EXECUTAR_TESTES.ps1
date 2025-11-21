# Script PowerShell para executar testes
# Execute: .\EXECUTAR_TESTES.ps1

Write-Host " Executando Testes do Projeto" -ForegroundColor Cyan
Write-Host ""

# Navega até a pasta src
$srcPath = Join-Path $PSScriptRoot "src"
Set-Location $srcPath

Write-Host " Diretório: $srcPath" -ForegroundColor Yellow
Write-Host ""

# Verifica se pytest está instalado
Write-Host " Verificando dependências..." -ForegroundColor Yellow
try {
    $pytestVersion = python -m pytest --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " pytest encontrado" -ForegroundColor Green
    } else {
        Write-Host " pytest não encontrado. Instalando..." -ForegroundColor Red
        pip install pytest pytest-asyncio httpx
    }
} catch {
    Write-Host " pytest não encontrado. Instalando..." -ForegroundColor Red
    pip install pytest pytest-asyncio httpx
}

Write-Host ""
Write-Host " Executando testes..." -ForegroundColor Cyan
Write-Host ""

# Executa os testes usando python -m pytest (funciona mesmo se pytest não estiver no PATH)
python -m pytest tests/ -v

Write-Host ""
Write-Host " Testes concluidos!" -ForegroundColor Green

