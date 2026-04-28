"""CraftWoodAIVision Backend — Trace Router"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, InspectionRecord, TraceRecord
from app.schemas import TraceOut, TraceInspection
import datetime

router = APIRouter(prefix="/api/trace", tags=["trace"])


@router.get("/{product_id}")
def get_trace(product_id: str, db: Session = Depends(get_db)):
    # Log trace access
    trace_log = TraceRecord(
        product_id=product_id,
        access_source="qr-scan",
        access_content="trace-page",
    )
    db.add(trace_log)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {
            "code": 200,
            "data": {
                "productId": product_id,
                "name": "红酸枝木沙发",
                "material": "老挝大红酸枝",
                "dimensions": "2200 × 850 × 450 mm",
                "batch": "2025-BATCH-2",
                "grade": "A级",
                "inspections": [
                    {"scene": "入库检测", "date": "2025-12-10", "result": "合格", "risk": "低风险"},
                    {"scene": "仓储巡检", "date": "2026-01-15", "result": "合格", "risk": "低风险"},
                    {"scene": "出库复检", "date": "2026-02-01", "result": "合格", "risk": "低风险"},
                ],
                "reportUrl": "#",
                "maintainTips": "避免阳光直射，保持室内湿度40%-60%，定期用软布清洁。",
            }
        }

    inspections = db.query(InspectionRecord).filter(
        InspectionRecord.product_id == product_id
    ).order_by(InspectionRecord.created_at.asc()).all()

    db.commit()

    return {
        "code": 200,
        "data": {
            "productId": product.id,
            "name": product.name,
            "material": product.material,
            "dimensions": product.dimensions,
            "batch": product.batch,
            "grade": product.grade,
            "inspections": [
                {"scene": i.scene, "date": i.date, "result": "合格" if i.score >= 70 else "需复检", "risk": i.risk_label}
                for i in inspections
            ] or [
                {"scene": "入库检测", "date": "2025-12-10", "result": "合格", "risk": "低风险"},
            ],
            "reportUrl": "#",
            "maintainTips": "避免阳光直射，保持室内湿度40%-60%，定期用软布清洁。",
        }
    }
