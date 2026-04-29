# ============================================================
# CraftWoodAIVision · 匠木云检 — 一键启动脚本 (Windows PowerShell)
# ============================================================

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CraftWoodAIVision · 匠木云检" -ForegroundColor Cyan
Write-Host "  一键启动脚本 (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ---- Docker 模式 ----
if (Get-Command "docker" -ErrorAction SilentlyContinue) {
    Write-Host "[INFO] 检测到 Docker，正在启动全部服务..." -ForegroundColor Cyan
    docker compose up -d
    Write-Host ""
    Write-Host "[OK] 服务已启动：" -ForegroundColor Green
    Write-Host "[OK]   前端后台  → http://localhost" -ForegroundColor Green
    Write-Host "[OK]   API 服务  → http://localhost:8080" -ForegroundColor Green
    Write-Host "[OK]   API 文档  → http://localhost:8080/docs" -ForegroundColor Green
    Write-Host ""
    Write-Host "查看日志: docker compose logs -f" -ForegroundColor Cyan
    Write-Host "停止服务: docker compose down" -ForegroundColor Cyan
    Read-Host "按 Enter 退出"
    exit 0
}

# ---- 手动模式 ----
Write-Host "[WARN] 未检测到 Docker，尝试手动启动..." -ForegroundColor Yellow
Write-Host ""

# 检查依赖
$missing = $false
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] 未找到 Python，请先安装" -ForegroundColor Red
    $missing = $true
}
if (-not (Get-Command "node" -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] 未找到 Node.js，请先安装" -ForegroundColor Red
    $missing = $true
}
if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] 未找到 npm，请先安装" -ForegroundColor Red
    $missing = $true
}
if ($missing) { Read-Host "按 Enter 退出"; exit 1 }

# 启动后端
Write-Host "[INFO] 启动后端服务..." -ForegroundColor Cyan
Set-Location "$ProjectRoot\backend"

if (-not (Test-Path ".venv")) {
    Write-Host "[INFO] 创建 Python 虚拟环境..." -ForegroundColor Cyan
    python -m venv .venv
}

& ".venv\Scripts\Activate.ps1"
pip install -q -r requirements.txt

$backendJob = Start-Job -Name "CraftWood-Backend" -ScriptBlock {
    param($dir)
    Set-Location $dir
    & ".venv\Scripts\Activate.ps1"
    uvicorn app.main:app --reload --port 8080
} -ArgumentList (Get-Location).Path

Write-Host "[OK] 后端已启动 → http://localhost:8080" -ForegroundColor Green
Set-Location $ProjectRoot

# 启动前端
Write-Host "[INFO] 启动前端开发服务器..." -ForegroundColor Cyan
Set-Location "$ProjectRoot\frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "[INFO] 安装前端依赖..." -ForegroundColor Cyan
    npm install
}

$frontendJob = Start-Job -Name "CraftWood-Frontend" -ScriptBlock {
    param($dir)
    Set-Location $dir
    npm run dev
} -ArgumentList (Get-Location).Path

Write-Host "[OK] 前端已启动 → http://localhost" -ForegroundColor Green
Set-Location $ProjectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  前端: http://localhost" -ForegroundColor Green
Write-Host "  后端: http://localhost:8080" -ForegroundColor Green
Write-Host "  API 文档: http://localhost:8080/docs" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "按 Enter 停止所有服务..." -ForegroundColor Cyan
Read-Host

# 清理
Write-Host "[INFO] 正在停止服务..." -ForegroundColor Cyan
$backendJob | Stop-Job | Remove-Job
$frontendJob | Stop-Job | Remove-Job
Write-Host "[OK] 服务已停止" -ForegroundColor Green
