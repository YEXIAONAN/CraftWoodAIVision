#!/usr/bin/env bash
# ============================================================
# CraftWoodAIVision · 匠木云检 — 一键启动脚本
# 支持: Docker Compose | 手动启动 (macOS / Linux)
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${CYAN}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  CraftWoodAIVision · 匠木云检${NC}"
echo -e "${CYAN}  一键启动脚本${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# ---- Docker 模式 ----
if command -v docker &> /dev/null && docker compose version &> /dev/null; then
    log_info "检测到 Docker，正在启动全部服务..."
    docker compose up -d
    echo ""
    log_ok "服务已启动："
    log_ok "  前端后台  → http://localhost"
    log_ok "  API 服务  → http://localhost:8080"
    log_ok "  API 文档  → http://localhost:8080/docs"
    log_ok "  MinIO 管理 → http://localhost:9001"
    echo ""
    log_info "查看日志: docker compose logs -f"
    log_info "停止服务: docker compose down"
    exit 0
fi

# ---- 手动模式 ----
log_warn "未检测到 Docker，尝试手动启动..."
echo ""

# 检查依赖
check_dep() {
    if ! command -v "$1" &> /dev/null; then
        log_error "未找到 $1，请先安装"
        exit 1
    fi
    log_ok "$1 已安装"
}

check_dep "python3"
check_dep "node"
check_dep "npm"

# 启动后端
log_info "启动后端服务..."
cd "$PROJECT_DIR/backend"

if [ ! -d ".venv" ]; then
    log_info "创建 Python 虚拟环境..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

uvicorn app.main:app --reload --port 8080 &
BACKEND_PID=$!
log_ok "后端已启动 (PID: $BACKEND_PID) → http://localhost:8080"
cd "$PROJECT_DIR"

# 启动前端
log_info "启动前端开发服务器..."
cd "$PROJECT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    log_info "安装前端依赖..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
log_ok "前端已启动 (PID: $FRONTEND_PID) → http://localhost"

cd "$PROJECT_DIR"
echo ""
log_ok "========================================"
log_ok "  前端: http://localhost"
log_ok "  后端: http://localhost:8080"
log_ok "  API 文档: http://localhost:8080/docs"
log_ok "========================================"
echo ""
log_info "按 Ctrl+C 停止所有服务"

# 捕获退出信号
cleanup() {
    echo ""
    log_info "正在停止服务..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    log_ok "服务已停止"
    exit 0
}
trap cleanup SIGINT SIGTERM

# 等待子进程
wait
