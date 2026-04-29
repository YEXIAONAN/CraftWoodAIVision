![CraftWoodAIVision](https://socialify.git.ci/YEXIAONAN/CraftWoodAIVision/image?font=Source+Code+Pro&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F89679677%3Fs%3D400%26u%3Da5ecde5dfa8566b1982ff841ae5e2f44da29c145%26v%3D4&name=1&owner=1&pattern=Circuit+Board&theme=Light)

# CraftWoodAIVision · 匠木云检

> AI 赋能 · 智能质检与溯源平台  
> 面向红木家具行业的质量管理与可信追溯系统

CraftWoodAIVision 是一个面向红木家具生产、仓储、销售与售后场景的智能质检与可信履历平台。系统以 **"AI 辅助质检 + 数字化质量档案 + 二维码可信追溯"** 为核心，将传统依赖人工经验的质检流程重构为可记录、可复核、可追溯、可统计的数字化质量管理体系。

---

## 目录

- [功能总览](#功能总览)
- [技术栈](#技术栈)
- [系统架构](#系统架构)
- [快速开始](#快速开始)
  - [环境要求](#环境要求)
  - [Docker 一键部署（推荐）](#docker-一键部署推荐)
  - [手动启动（开发模式）](#手动启动开发模式)
- [数据库初始化](#数据库初始化)
- [项目结构](#项目结构)
- [API 文档](#api-文档)
- [设计主题](#设计主题)
- [开发指南](#开发指南)
- [分支说明](#分支说明)
- [License](#license)

---

## 功能总览

| 模块 | 功能 | 面向用户 |
|------|------|---------|
| **工作台** | 质检数据概览、KPI 指标展示、缺陷分布图表、周趋势分析 | 管理员 / 质检员 |
| **产品档案** | 产品建档、信息管理、二维码追溯入口 | 管理员 / 销售 |
| **AI 质检** | 图片上传/拍摄、缺陷识别、风险评分、结果复核 | 质检员 |
| **出入库管理** | 入库登记、仓储巡检、出库复检、库存状态流转 | 仓库管理员 |
| **质检报告** | 自动生成检测报告、报告下载、历史存档 | 质检员 |
| **售后管理** | 售后工单提交、处理进度跟踪、责任追溯 | 售后专员 |
| **数据大屏** | 全平台质量数据实时监控、多维度可视化分析 | 管理层 |
| **二维码追溯** | 消费者扫码查看产品质检档案（公开页面） | 终端消费者 |

---

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **前端** | Vue 3 (Composition API) + TypeScript + Vite 6 | 应用框架 |
| **UI 组件** | Element Plus + ECharts (vue-echarts) | 后台 UI / 数据可视化 |
| **状态管理** | Pinia | 全局状态（用户认证、应用配置） |
| **路由** | Vue Router 4 | 前端路由 + 导航守卫 |
| **后端** | FastAPI + Python 3.12 | RESTful API 服务 |
| **ORM** | SQLAlchemy 2.0 + Alembic | 数据库 ORM 与迁移 |
| **数据校验** | Pydantic v2 | 请求/响应模型校验 |
| **认证** | JWT (python-jose) + bcrypt | 无状态认证 + RBAC |
| **数据库** | MySQL 8.0 | 业务数据存储 |
| **缓存** | Redis 7 | 会话缓存 / 热点数据 |
| **对象存储** | MinIO | 质检图片 / 报告文件存储 |
| **AI 推理** | YOLOv8/v11 + PyTorch + ONNX Runtime | 表面缺陷检测 |
| **容器化** | Docker + Docker Compose | 部署与编排 |

---

## 系统架构

```
┌─────────┐     ┌──────────────┐     ┌──────────┐
│ Browser │────▶│ Vite 开发服务器 │────▶│ FastAPI  │
│ :80     │     │ (npm run dev) │     │ :8080    │
└─────────┘     └──────────────┘     └────┬─────┘
                                           │
          ┌────────────────────────────────┼──────────────────────┐
          │                                │                      │
          ▼                                ▼                      ▼
   ┌──────────┐                     ┌──────────────┐      ┌────────────┐
   │  MySQL   │                     │    Redis     │      │   MinIO    │
   │  :3306   │                     │   :6379      │      │ :9000/9001 │
   └──────────┘                     └──────────────┘      └────────────┘
```

### 组件说明

| 组件 | 用途 | 为什么需要 |
|------|------|-----------|
| **Vite** | 前端开发服务器，托管 Vue 页面并代理 API 请求 | `npm run dev` 自带热重载，无需额外 Web 服务器 |
| **FastAPI** | Python 后端，提供 RESTful API | 处理业务逻辑、数据存取、AI 推理调度 |
| **MySQL** | 关系型数据库，存储核心业务数据 | 产品档案、质检记录、报告、工单等结构化数据 |
| **Redis** | 内存缓存数据库 | 缓存热点数据（如大屏统计）、加速查询、暂存验证码/会话状态 |
| **MinIO** | 对象存储服务（类似 AWS S3） | 存储上传的质检图片、缺陷标注图、生成的 PDF 报告 |

### 数据状态流转

```
入库 ──▶ 仓储中 ──▶ 待出库 ──▶ 已出库 ──▶ 已归档
  │                    │            │
  ▼                    ▼            ▼
入库检测            仓储巡检      出库复检
```

### RBAC 权限模型

| 角色 | 权限范围 |
|------|---------|
| `admin` | 全部管理权限 |
| `inspector` | 质检操作、报告查看 |
| `sales` | 产品档案、售后管理 |
| `consumer` | 仅二维码追溯页面（公开） |

---

## 快速开始

### 环境要求

- **Docker** + Docker Compose（推荐部署方式）
- 或手动安装：**Node.js 20+**、**Python 3.12+**、**MySQL 8.0**、**Redis 7**

### Docker 一键部署（推荐）

```bash
# 启动全部服务
docker compose up -d

# 查看运行状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

部署后访问：
- 前端管理后台：http://localhost
- API 服务：http://localhost:8080
- API 文档：http://localhost:8080/docs
- MinIO 控制台：http://localhost:9001

### 手动启动（开发模式）

#### 1. 数据库与缓存

确保 MySQL 和 Redis 已启动，然后创建数据库：

```bash
mysql -uroot -p -e "CREATE DATABASE IF NOT EXISTS craftwood CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

> 详细数据库初始化步骤见 [数据库初始化](#数据库初始化) 章节。

#### 2. 后端

```bash
cd backend

# 创建虚拟环境（可选）
python -m venv .venv && source .venv/bin/activate  # macOS/Linux
# 或: .venv\Scripts\activate                       # Windows

# 安装依赖
pip install -r requirements.txt

# 启动 API 服务（默认端口 8080）
uvicorn app.main:app --reload --port 8080
```

首次启动会自动创建数据表并写入示例种子数据（默认管理员账号见下方）。

#### 3. 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器 → http://localhost
npm run dev
```

#### 默认管理员账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `admin123` | 管理员 |

---

## 数据库初始化

### 方式一：使用 SQL 脚本导入（推荐）

项目提供了完整的建表脚本 `backend/sql/init.sql`。

```bash
# 1. 确保 MySQL 已启动
mysql -uroot -p

# 2. 执行建表脚本（在 MySQL 提示符下）
mysql> source /path/to/CraftWoodAIVision/backend/sql/init.sql;
# 或直接在终端执行：
mysql -uroot -p < backend/sql/init.sql

# 3. 验证数据库创建成功
mysql> SHOW DATABASES;
mysql> USE craftwood;
mysql> SHOW TABLES;
```

### 方式二：通过 Docker Compose 自动初始化

使用 Docker Compose 启动时，MySQL 容器会自动创建 `craftwood` 数据库。应用启动时（`app/main.py` 的 `lifespan` 事件）会自动执行以下操作：

1. 调用 `Base.metadata.create_all()` 创建所有 ORM 映射的表结构
2. 调用 `seed_database()` 写入管理员账号和示例数据

### 方式三：通过应用自动建表

手动启动后端时，应用启动后会自动：
- 检查数据库中是否已有用户数据
- 若无数据则自动建表并写入种子数据
- 已有数据则跳过初始化

### 数据表一览

| 表名 | 说明 | 核心字段 |
|------|------|---------|
| `user` | 用户与角色 | username, hashed_password, role |
| `product` | 产品档案 | id(PROD-N), name, type, status, grade |
| `inspection_record` | 质检记录 | id(INS-N), product_id, scene, risk, score, defects(JSON) |
| `warehouse_record` | 出入库记录 | id(WH-N), product_id, action, operator |
| `report_record` | 质检报告 | id(RPT-N), product_id, conclusion, score |
| `after_sales_record` | 售后工单 | id(AS-N), product_id, type, status |
| `trace_record` | 扫码追溯日志 | product_id, access_time, access_source |

---

## 项目结构

```
CraftWoodAIVision/
├── frontend/                      # Vue 3 前端应用
│   ├── src/
│   │   ├── api/                   # Axios 客户端 + API 接口封装
│   │   ├── assets/                # SVG 资源（木纹、回纹等）
│   │   ├── components/
│   │   │   ├── common/            # 公共组件（StatCard, DefectTag, StatusBadge）
│   │   │   └── layout/            # 布局组件（AppLayout, AppHeader, AppSidebar）
│   │   ├── mock/                  # Mock 数据层（开发阶段使用）
│   │   ├── router/                # 路由配置 + 导航守卫
│   │   ├── stores/                # Pinia 状态（auth, app）
│   │   ├── styles/                # 全局样式
│   │   ├── types/                 # TypeScript 类型定义
│   │   └── views/                 # 11 个页面视图
│   ├── Dockerfile                 # 多阶段构建（Nginx 运行）
│   └── nginx.conf                 # Nginx 反向代理配置
│
├── backend/                       # FastAPI 后端服务
│   ├── app/
│   │   ├── main.py                # 应用入口（lifespan, CORS, 路由注册）
│   │   ├── config.py              # 配置（数据库、JWT、上传限制）
│   │   ├── database.py            # SQLAlchemy 引擎与会话
│   │   ├── models.py              # 7 个 ORM 模型
│   │   ├── schemas.py             # Pydantic 请求/响应模型
│   │   ├── security.py            # JWT 生成/验证 + bcrypt 密码
│   │   ├── deps.py                # FastAPI 依赖注入（get_current_user）
│   │   ├── seed.py                # 种子数据填充
│   │   └── routers/               # 8 个 API 路由模块
│   ├── sql/
│   │   └── init.sql               # MySQL 建表脚本
│   ├── requirements.txt
│   └── Dockerfile                 # Python 3.12-slim
│
├── docker/                        # Docker 配置文件
│   ├── redis/
│   │   ├── Dockerfile              # Redis 自定义镜像
│   │   └── redis.conf              # Redis 持久化与缓存策略
│   └── minio/
│       ├── config.env              # MinIO 管理员账号配置
│       └── entrypoint.sh           # MinIO 启动时自动创建 bucket
├── docs/                          # 技术文档
│   ├── README.md                  # 文档索引
│   ├── frontend.md                # 前端技术说明
│   ├── backend.md                 # 后端技术说明
│   ├── ai-ml.md                   # AI/ML 技术说明
│   ├── database.md                # 数据库设计说明
│   └── devops.md                  # DevOps 部署说明
│
├── start.sh                       # 一键启动脚本（macOS / Linux）
├── start.bat                      # 一键启动脚本（Windows CMD）
├── start.ps1                      # 一键启动脚本（Windows PowerShell）
├── docker-compose.yml             # Docker 编排配置
├── .github/workflows/             # GitHub Actions CI/CD
│   ├── frontend-ci.yml
│   └── backend-ci.yml
├── README.md
└── LICENSE
```

---

## API 文档

启动后端后访问以下地址查看自动生成的 OpenAPI 文档：

- **Swagger UI**：http://localhost:8080/docs
- **ReDoc**：http://localhost:8080/redoc

### 核心 API 路由

| 模块 | 前缀 | 主要端点 |
|------|------|---------|
| Auth | `/api/auth` | POST `/login`, GET `/me` |
| Products | `/api/products` | GET `/`, POST `/`, GET `/{id}` |
| Inspections | `/api/inspections` | GET `/`, POST `/`, GET `/{id}` |
| Warehouse | `/api/warehouse` | CRUD 完整操作 |
| Reports | `/api/reports` | CRUD + GET `/{id}/download` |
| After-Sales | `/api/after-sales` | CRUD + PUT `/{id}/{process\|complete\|close}` |
| Trace | `/api/trace` | GET `/{productId}`（公开，无需认证） |
| Dashboard | `/api/dashboard` | GET `/stats` |

---

## 设计主题

- **品牌调性**：红木家具 · 匠心传承 · 智能科技
- **主色调**：红木色 `#9B3A1C` / `#8B4513`
- **辅色调**：古铜金 `#C9A063`
- **背景色**：宣纸白 `#F7F4EB`
- **视觉风格**：现代数据大屏 + 新中式轻奢
- **Element Plus 主题**：在 `App.vue` 中通过 CSS 变量覆盖实现统一风格

---

## 开发指南

### 前端开发

```bash
cd frontend
npm run dev          # 开发服务器（热重载）
npm run build        # 生产构建 → dist/
npm run typecheck    # TypeScript 类型检查
npm run preview      # 预览生产构建
```

- 使用 Composition API + `<script setup>` 语法
- API 接口统一在 `src/api/index.ts` 中封装
- Mock 数据在 `src/mock/index.ts`，开发阶段直接返回本地数据
- 路由懒加载，生产构建自动分包（Vue/ECharts/Element Plus 分离）

### 后端开发

```bash
cd backend
uvicorn app.main:app --reload --port 8080
```

- 路由注册在 `app/main.py`，新增模块需在此注册
- Pydantic 模型使用 `from_attributes = True` + `populate_by_name = True` 支持 ORM 映射
- 统一响应格式：`{"code": 200, "data": ..., "message": "..."}`
- 所有管理端 API 默认需要 JWT 认证（除 `/api/auth/login` 和 `/api/trace`）
- 种子数据在 `app/seed.py`，首次启动自动填充

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | 数据库连接地址 | `mysql+pymysql://root:123456@localhost:3306/craftwood` |
| `REDIS_URL` | Redis 连接地址 | `redis://redis:6379/0` |
| `SECRET_KEY` | JWT 密钥 | `craftwood-dev-secret-key-...` |
| `DEBUG` | 调试模式 | `true` |

### CI/CD

项目使用 GitHub Actions 进行持续集成：

- **Frontend CI**：`npm ci` → `vue-tsc --noEmit` → `npm run build` → 验证 dist 输出
- **Backend CI**：pip 安装依赖 → 验证模块导入 → 运行 pytest（如果存在测试）

---

## 分支说明

| 分支 | 用途 |
|------|------|
| `main` | 主分支，稳定版本 |
| `VisualRecognition` | AI 视觉识别模型训练与推理开发 |
| `Front-EndDevelopment` | 前端功能开发与优化 |
| `BackendDevelopment` | 后端 API 与业务逻辑开发 |

---

## License

MIT
