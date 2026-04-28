# Backend Tech Stack

## FastAPI
- **Role**: Business API, model inference interface, file upload
- **Why**: Async-friendly, high performance, auto-generated OpenAPI docs
- Deployment: Uvicorn / Gunicorn

## SQLAlchemy + Alembic
- **Role**: ORM and database migration
- **Why**: Mature ORM with migration support
- Manages core tables: product, inspection, report, trace, after-sales

## JWT + RBAC
- **Role**: Stateless authentication and role-based access control
- **Roles**: Admin, Inspector, Sales, Consumer (QR page)
- **Principle**: Minimal privilege, default-deny for all admin APIs

## Core API Modules

| Module | Endpoints |
|--------|-----------|
| Auth | Login, token refresh, logout |
| Product | CRUD, QR code generation |
| Inspection | Image upload, AI inference trigger, result review |
| Report | Auto-generated report, download |
| Warehouse | Inbound, storage巡检, outbound |
| Trace | QR scan page data, access log |
| After-Sales | Issue submission, history comparison |
| Dashboard | Aggregated stats and chart data |

## Security

| Dimension | Implementation |
|-----------|---------------|
| Auth | JWT with expiration, hashed passwords |
| Authorization | RBAC — admin, inspector, sales, consumer |
| API Security | Param validation, file type/size check, rate limiting |
| Data Security | Sensitive field masking, DB backup, object storage ACL |
| Audit | Key operation logging (user, time, IP, action) |
