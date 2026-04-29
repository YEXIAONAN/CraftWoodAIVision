#!/bin/sh
# ============================================================
# CraftWoodAIVision · 匠木云检 — MinIO 启动脚本
# 自动创建所需的 bucket
# ============================================================

set -e

# 启动 MinIO 服务
minio server /data --console-address ":9001" &

# 等待服务就绪
sleep 3

# 配置 alias
mc alias set craftwood http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

# 创建 bucket
mc mb craftwood/inspection-images --ignore-existing
mc mb craftwood/inspection-annotated --ignore-existing
mc mb craftwood/reports --ignore-existing
mc mb craftwood/trace --ignore-existing

# 设置 bucket 访问策略（trace 公开只读，其余私有）
mc anonymous set download craftwood/trace
mc anonymous set private craftwood/inspection-images
mc anonymous set private craftwood/inspection-annotated
mc anonymous set private craftwood/reports

echo "=== MinIO buckets initialized ==="

# 等待后台进程
wait
