"""CraftWoodAIVision Backend — Warehouse Router"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import WarehouseRecord, User
from app.schemas import WarehouseOut
from app.deps import get_current_user

router = APIRouter(prefix="/api/warehouse", tags=["warehouse"])


@router.get("")
def list_warehouse(
    action: str = Query("", max_length=16),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(WarehouseRecord)
    if action:
        q = q.filter(WarehouseRecord.action == action)
    total = q.count()
    items = q.order_by(WarehouseRecord.created_at.desc()).all()
    return {
        "code": 200,
        "data": {
            "list": [WarehouseOut.model_validate(r) for r in items],
            "total": total,
        }
    }
