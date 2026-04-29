![img](.images\CraftWoodAIVision.png)
# CraftWoodAIVision · 匠木云检

CraftWoodAIVision 是一个面向红木家具生产、仓储、销售与售后场景的智能质检与可信履历平台。系统以"AI 辅助质检 + 数字化质量档案 + 二维码可信追溯"为核心，将传统依赖人工经验的质检流程重构为可记录、可复核、可追溯、可统计的数字化质量管理体系。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + TypeScript + Element Plus |
| 状态管理 | Pinia |
| 路由 | Vue Router 4 |
| 图表 | ECharts (vue-echarts) |
| 后端 | FastAPI + SQLAlchemy + Alembic |
| 数据库 | MySQL + Redis + MinIO |
| AI 模型 | YOLOv8/v11 + PyTorch + ONNX Runtime |
| 部署 | Docker + Docker Compose + Nginx |

## 功能模块

- **工作台** — 质检数据概览与趋势分析
- **产品档案** — 产品数字建档与二维码追溯
- **AI 质检** — 图片上传、缺陷识别与风险评分
- **出入库管理** — 入库、仓储巡检、出库复检全流程
- **质检报告** — 自动生成检测报告
- **售后管理** — 售后工单与责任追溯
- **数据大屏** — 全平台数据实时监控

## 快速开始

### 前端

```bash
cd frontend
npm install
npm run dev        # 开发服务器 → http://localhost:5173
npm run build      # 生产构建
```

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload    # API 服务 → http://localhost:8000
```

### Docker 部署

```bash
docker compose up -d
```

## 项目结构

```
CraftWoodAIVision/
├── frontend/                # Vue 3 前端应用
│   ├── src/
│   │   ├── api/             # API 接口层（当前为 Mock 数据）
│   │   ├── assets/          # 资源文件（SVG、图片）
│   │   ├── components/      # 公共组件
│   │   ├── mock/            # Mock 数据
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── styles/          # 全局样式
│   │   └── views/           # 页面视图
│   ├── Dockerfile
│   └── nginx.conf
├── backend/                 # FastAPI 后端服务（开发中）
│   ├── app/
│   │   └── main.py          # 应用入口
│   ├── requirements.txt
│   └── Dockerfile
├── docs/                    # 技术文档
├── docker-compose.yml
├── README.md
└── LICENSE
```

## 设计主题

- **品牌调性**：红木家具 · 匠心传承 · 智能科技
- **配色方案**：红木主色 `#9B3A1C` · 古铜金 `#C9A063` · 宣纸白 `#F7F4EB`
- **视觉风格**：现代数据大屏 + 新中式轻奢

## License

MIT
