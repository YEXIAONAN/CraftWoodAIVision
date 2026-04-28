# Database & Storage Tech Stack

## MySQL
- **Role**: Structured business data storage
- **Why**: ACID transactions, reliable for core business data
- **Key Tables**:

| Table | Purpose |
|-------|---------|
| `user` | Users, roles, permissions, login status |
| `product` | Product digital identity (ID, name, type, dimensions, batch, status) |
| `inspection_record` | Inspection main record (time, inspector, scenario, risk level, score) |
| `defect_record` | Defect details (category, coordinates, confidence, area, status) |
| `warehouse_record` | Inbound, storage巡检, outbound, status transitions |
| `report_record` | Inspection report archive |
| `trace_record` | QR scan access log (time, source, content) |
| `after_sales_record` | After-sales issue, images, progress, responsibility assessment |

## Redis
- **Role**: High-performance cache and temporary state
- **Use Cases**: Verification codes, login session cache, hot trace data, async task status

## MinIO / Local Object Storage
- **Role**: Large-volume image and report file storage
- **Stored Assets**: Raw images, annotated images, report attachments, trace materials
- **Optimization**: Tiered storage (original / thumbnail / annotated), compressed images for trace page

## Data Consistency

- Idempotency for outbound re-inspection, report generation, QR creation
- Finite state machine for product status transitions:
  `Inbound → In Storage → Ready → Outbound → Archived`
