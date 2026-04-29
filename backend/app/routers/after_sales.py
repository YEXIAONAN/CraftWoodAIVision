"""CraftWoodAIVision Backend — After-Sales Router"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AfterSalesRecord, User
from app.schemas import AfterSalesOut, AfterSalesCreate, AfterSalesUpdate
from app.deps import get_current_user

router = APIRouter(prefix="/api/after-sales", tags=["after-sales"])


def _now_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


@router.get("")
def list_after_sales(
    status: str = Query("", max_length=16),
    keyword: str = Query("", max_length=64),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(AfterSalesRecord)
    if status:
        q = q.filter(AfterSalesRecord.status == status)
    if keyword:
        q = q.filter(
            (AfterSalesRecord.product_name.contains(keyword)) |
            (AfterSalesRecord.product_id.contains(keyword)) |
            (AfterSalesRecord.customer.contains(keyword))
        )
    total = q.count()
    items = q.order_by(AfterSalesRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "code": 200,
        "data": {
            "list": [AfterSalesOut.model_validate(r) for r in items],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }
    }


@router.post("")
def create_after_sales(data: AfterSalesCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    count = db.query(AfterSalesRecord).count()
    as_record = AfterSalesRecord(
        id=f"AS-{count + 1:04d}",
        product_id=data.product_id,
        product_name=data.product_name,
        type=data.type,
        description=data.description,
        customer=data.customer,
        status="待处理",
        date=_now_str(),
    )
    db.add(as_record)
    db.commit()
    db.refresh(as_record)
    return {"code": 200, "data": AfterSalesOut.model_validate(as_record), "message": "工单创建成功"}


@router.put("/{record_id}")
def update_after_sales(record_id: str, data: AfterSalesUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    as_record = db.query(AfterSalesRecord).filter(AfterSalesRecord.id == record_id).first()
    if not as_record:
        return {"code": 404, "message": "工单不存在", "data": None}
    updates = data.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(as_record, k, v)
    db.commit()
    db.refresh(as_record)
    return {"code": 200, "data": AfterSalesOut.model_validate(as_record), "message": "更新成功"}


@router.delete("/{record_id}")
def delete_after_sales(record_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    as_record = db.query(AfterSalesRecord).filter(AfterSalesRecord.id == record_id).first()
    if not as_record:
        return {"code": 404, "message": "工单不存在", "data": None}
    db.delete(as_record)
    db.commit()
    return {"code": 200, "message": "删除成功"}


@router.put("/{record_id}/process")
def process_after_sales(record_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    as_record = db.query(AfterSalesRecord).filter(AfterSalesRecord.id == record_id).first()
    if not as_record:
        return {"code": 404, "message": "工单不存在", "data": None}
    if as_record.status != "待处理":
        return {"code": 400, "message": "仅待处理状态的工单可以开始处理"}
    as_record.status = "处理中"
    as_record.handler = user.name
    db.commit()
    db.refresh(as_record)
    return {"code": 200, "data": AfterSalesOut.model_validate(as_record), "message": "已开始处理"}


@router.put("/{record_id}/complete")
def complete_after_sales(record_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    as_record = db.query(AfterSalesRecord).filter(AfterSalesRecord.id == record_id).first()
    if not as_record:
        return {"code": 404, "message": "工单不存在", "data": None}
    if as_record.status != "处理中":
        return {"code": 400, "message": "仅处理中状态的工单可以标记完成"}
    as_record.status = "已完成"
    db.commit()
    db.refresh(as_record)
    return {"code": 200, "data": AfterSalesOut.model_validate(as_record), "message": "工单已完成"}


@router.put("/{record_id}/close")
def close_after_sales(record_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    as_record = db.query(AfterSalesRecord).filter(AfterSalesRecord.id == record_id).first()
    if not as_record:
        return {"code": 404, "message": "工单不存在", "data": None}
    as_record.status = "已关闭"
    db.commit()
    db.refresh(as_record)
    return {"code": 200, "data": AfterSalesOut.model_validate(as_record), "message": "工单已关闭"}
