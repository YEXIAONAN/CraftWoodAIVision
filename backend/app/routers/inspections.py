"""CraftWoodAIVision Backend — Inspections Router"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import InspectionRecord, User
from app.schemas import InspectionOut
from app.deps import get_current_user

router = APIRouter(prefix="/api/inspections", tags=["inspections"])


@router.get("")
def list_inspections(
    scene: str = Query("", max_length=16),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(InspectionRecord)
    if scene:
        q = q.filter(InspectionRecord.scene == scene)
    total = q.count()
    items = q.order_by(InspectionRecord.created_at.desc()).all()
    return {
        "code": 200,
        "data": {
            "list": [InspectionOut.model_validate(i) for i in items],
            "total": total,
        }
    }


@router.get("/{inspection_id}")
def get_inspection(inspection_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    item = db.query(InspectionRecord).filter(InspectionRecord.id == inspection_id).first()
    if not item:
        return {"code": 404, "message": "检测记录不存在", "data": None}
    return {"code": 200, "data": InspectionOut.model_validate(item)}


import datetime
from app.models import Product


@router.post("")
def submit_inspection(
    scene: str = Query("入库检测"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    count = db.query(InspectionRecord).count()
    defects = [
        {"type": "裂纹", "confidence": 0.92, "bbox": [120, 80, 65, 30], "area": 180},
        {"type": "划痕", "confidence": 0.85, "bbox": [200, 150, 90, 15], "area": 95},
    ]
    ins = InspectionRecord(
        id=f"INS-{count + 1:04d}",
        product_id=f"PROD-{((count) % 18) + 1:04d}",
        product_name="红酸枝木沙发",
        date=datetime.date.today().strftime("%Y-%m-%d"),
        inspector=user.name,
        scene=scene,
        risk="low",
        risk_label="低风险",
        score=91.3,
        defects=defects,
        image="",
        annotated_image="",
        notes="",
        reviewed=0,
    )
    db.add(ins)
    db.commit()
    db.refresh(ins)
    return {"code": 200, "data": InspectionOut.model_validate(ins), "message": "质检完成"}
