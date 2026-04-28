"""CraftWoodAIVision Backend — Reports Router"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ReportRecord, User
from app.schemas import ReportOut
from app.deps import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("")
def list_reports(
    keyword: str = Query("", max_length=64),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(ReportRecord)
    if keyword:
        q = q.filter(ReportRecord.product_name.contains(keyword))
    total = q.count()
    items = q.order_by(ReportRecord.created_at.desc()).all()
    return {
        "code": 200,
        "data": {
            "list": [ReportOut.model_validate(r) for r in items],
            "total": total,
        }
    }


@router.get("/{report_id}")
def get_report(report_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rpt = db.query(ReportRecord).filter(ReportRecord.id == report_id).first()
    if not rpt:
        return {"code": 404, "message": "报告不存在", "data": None}
    return {"code": 200, "data": ReportOut.model_validate(rpt)}
