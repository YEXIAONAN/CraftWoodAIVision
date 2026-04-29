@echo off
REM ============================================================
REM CraftWoodAIVision · 匠木云检 — 一键启动脚本 (Windows CMD)
REM ============================================================

cd /d "%~dp0"

echo ========================================
echo   CraftWoodAIVision · 匠木云检
echo   一键启动脚本 (Windows)
echo ========================================
echo.

REM ---- Docker 模式 ----
where docker >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] 检测到 Docker，正在启动全部服务...
    docker compose up -d
    echo.
    echo [OK] 服务已启动：
    echo [OK]   前端后台  -^> http://localhost
    echo [OK]   API 服务  -^> http://localhost:8080
    echo [OK]   API 文档  -^> http://localhost:8080/docs
    echo.
    echo 查看日志: docker compose logs -f
    echo 停止服务: docker compose down
    pause
    exit /b 0
)

REM ---- 手动模式 ----
echo [WARN] 未检测到 Docker，尝试手动启动...
echo.

REM 启动后端
echo [INFO] 启动后端服务...
cd backend

if not exist ".venv" (
    echo [INFO] 创建 Python 虚拟环境...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo [INFO] 后端: http://localhost:8080
start "CraftWood-Backend" cmd /c "uvicorn app.main:app --reload --port 8080"
cd ..

REM 启动前端
echo [INFO] 启动前端开发服务器...
cd frontend

if not exist "node_modules" (
    echo [INFO] 安装前端依赖...
    npm install
)

echo [INFO] 前端: http://localhost
start "CraftWood-Frontend" cmd /c "npm run dev"
cd ..

echo.
echo ========================================
echo   前端: http://localhost
echo   后端: http://localhost:8080
echo   API 文档: http://localhost:8080/docs
echo ========================================
echo.
echo 请关闭命令行窗口以停止服务
pause
