# DevOps & Infrastructure Tech Stack

## Containerization

| Component | Technology |
|-----------|-----------|
| Frontend | Nginx (static file serving) |
| Backend | FastAPI + Uvicorn / Gunicorn |
| Database | MySQL |
| Cache | Redis |
| File Storage | MinIO or local object storage |
| Orchestration | Docker Compose |

## CI/CD Pipeline

```
Code Commit → Dependency Install → Lint → Unit Test → Build
                ↓
    Frontend: static build   Backend: Docker image
                ↓
        Deploy to demo environment
```

## Best Practices

- Git branch management (feature / dev / main)
- Issue task breakdown
- Pull Request code review
- Environment variable configuration management
- Database migration scripts (Alembic)
- Auto-generated API docs (OpenAPI/Swagger)

## Performance Optimization

| Layer | Strategy |
|-------|----------|
| Frontend | Route lazy loading, component on-demand import, image compression, pagination, ECharts lazy render |
| Backend | Async endpoints, DB index optimization, batch queries, pagination, Redis caching, separated file/structured storage |
| AI Inference | ONNX export, batch inference, image size normalization, independent deployment, optional GPU |
| File Storage | Tiered original/thumbnail/annotated storage, compressed images on trace page |

## Observability

| Type | Purpose |
|------|---------|
| Logs | API errors, model inference failures |
| Metrics | QPS, latency, error rate, CPU/GPU/memory usage |
| Tracing | End-to-end inspection request timing |

## Cloud-Native Evolution Path

```
MVP: Docker Compose → Growth: Kubernetes + Ingress + Service Mesh
                             →
         Message Queue + Centralized Logging + Auto-scaling
```
