"""CraftWoodAIVision Backend — Products Router"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, User
from app.schemas import ProductOut, ProductCreate
from app.deps import get_current_user

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
def list_products(
    keyword: str = Query("", max_length=64),
    status: str = Query("", max_length=16),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(Product)
    if keyword:
        q = q.filter((Product.name.contains(keyword)) | (Product.id.contains(keyword)))
    if status:
        q = q.filter(Product.status == status)
    total = q.count()
    items = q.all()
    return {
        "code": 200,
        "data": {
            "list": [ProductOut.model_validate(p) for p in items],
            "total": total,
        }
    }


@router.get("/{product_id}")
def get_product(product_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return {"code": 404, "message": "产品不存在", "data": None}
    return {"code": 200, "data": ProductOut.model_validate(product)}


@router.post("")
def create_product(data: ProductCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    count = db.query(Product).count()
    product = Product(
        id=f"PROD-{count + 1:04d}",
        name=data.name,
        type=data.type,
        material=data.material,
        dimensions=data.dimensions,
        batch=data.batch,
        inspector=data.inspector or _.name,
        status="已入库",
        grade="A级",
        date="",
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"code": 200, "data": ProductOut.model_validate(product), "message": "创建成功"}
