# Tech Stack — AI-Empowered · Smart Wood Inspection & Traceability Platform

> System Architecture: Frontend-Backend Separation + Modular Services + Independent AI Inference Service + Layered Data Governance

## Architecture Layers

| Layer | Technologies | Responsibility |
|-------|-------------|----------------|
| [User Interface](frontend.md) | Vue 3, Vite, TypeScript, Element Plus, Pinia, ECharts | Business operations, result display, QR scan, after-sales |
| [Application Service](backend.md) | FastAPI, SQLAlchemy, Alembic, JWT, RBAC | Core business RESTful APIs, auth, product/inspection/report/trace management |
| [AI Capability](ai-ml.md) | YOLOv8/v11, PyTorch, OpenCV, ONNX Runtime, SAM/CLIP | Defect detection, image preprocessing, risk scoring, annotated image generation |
| [Data Persistence](database.md) | MySQL, Redis, MinIO | Structured data, cache, image/file storage |
| [Infrastructure](devops.md) | Docker, Docker Compose, Nginx, CI/CD, Uvicorn/Gunicorn | Deployment, reverse proxy, monitoring, continuous delivery |

## Data Flow

```
User → Nginx → Vue SPA / QR Trace Page
                    ↓
            FastAPI REST API
            ↓       ↓       ↓
       MySQL    Redis    MinIO
            ↓
       AI Inference Service (ONNX/YOLO)
```

## Deployment Architecture (MVP)

```
Frontend (Nginx static) + Backend (Uvicorn) + AI Service (ONNX Runtime)
                         +
              MySQL + Redis + MinIO
                         +
              Docker Compose orchestration
```
