"""CraftWoodAIVision Backend — Warehouse Router"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import WarehouseRecord, Product, User
from app.schemas import WarehouseOut, WarehouseCreate, WarehouseUpdate
from app.deps import get_current_user

router = APIRouter(prefix="/api/warehouse", tags=["warehouse"])

ACTION_STATUS_MAP = {
    "入库": "已入库",
    "出库": "已出库",
}

STATUS_TRANSITIONS = {
    "已入库": ["仓储中", "待出库", "已出库", "已归档"],
    "仓储中": ["待出库", "已出库", "已归档"],
    "待出库": ["已出库", "已归档"],
    "已出库": ["已归档"],
}


def _now_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


@router.get("")
def list_warehouse(
    action: str = Query("", max_length=16),
    keyword: str = Query("", max_length=64),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(WarehouseRecord)
    if action:
        q = q.filter(WarehouseRecord.action == action)
    if keyword:
        q = q.filter(
            (WarehouseRecord.product_name.contains(keyword)) |
            (WarehouseRecord.product_id.contains(keyword))
        )
    total = q.count()
    items = q.order_by(WarehouseRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "code": 200,
        "data": {
            "list": [WarehouseOut.model_validate(r) for r in items],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }
    }


@router.post("")
def create_warehouse(data: WarehouseCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    count = db.query(WarehouseRecord).count()
    wh = WarehouseRecord(
        id=f"WH-{count + 1:04d}",
        product_id=data.product_id,
        product_name=data.product_name or (product.name if product else ""),
        action=data.action,
        operator=user.name,
        date=_now_str(),
        notes=data.notes,
        status="已完成",
    )
    db.add(wh)

    # Sync product status based on warehouse action
    if product and data.action in ACTION_STATUS_MAP:
        product.status = ACTION_STATUS_MAP[data.action]

    db.commit()
    db.refresh(wh)
    return {"code": 200, "data": WarehouseOut.model_validate(wh), "message": "记录创建成功"}


@router.put("/{record_id}")
def update_warehouse(record_id: str, data: WarehouseUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    wh = db.query(WarehouseRecord).filter(WarehouseRecord.id == record_id).first()
    if not wh:
        return {"code": 404, "message": "记录不存在", "data": None}
    updates = data.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(wh, k, v)
    db.commit()
    db.refresh(wh)
    return {"code": 200, "data": WarehouseOut.model_validate(wh), "message": "更新成功"}


@router.delete("/{record_id}")
def delete_warehouse(record_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    wh = db.query(WarehouseRecord).filter(WarehouseRecord.id == record_id).first()
    if not wh:
        return {"code": 404, "message": "记录不存在", "data": None}
    db.delete(wh)
    db.commit()
    return {"code": 200, "message": "删除成功"}
