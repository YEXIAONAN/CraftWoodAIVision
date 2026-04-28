"""CraftWoodAIVision Backend — After-Sales Router"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AfterSalesRecord, User
from app.schemas import AfterSalesOut
from app.deps import get_current_user

router = APIRouter(prefix="/api/after-sales", tags=["after-sales"])


@router.get("")
def list_after_sales(
    status: str = Query("", max_length=16),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(AfterSalesRecord)
    if status:
        q = q.filter(AfterSalesRecord.status == status)
    total = q.count()
    items = q.order_by(AfterSalesRecord.created_at.desc()).all()
    return {
        "code": 200,
        "data": {
            "list": [AfterSalesOut.model_validate(r) for r in items],
            "total": total,
        }
    }
