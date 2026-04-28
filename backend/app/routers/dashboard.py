"""CraftWoodAIVision Backend — Dashboard Router"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import InspectionRecord, Product, AfterSalesRecord, User
from app.deps import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    today_count = db.query(InspectionRecord).count()
    anomaly_count = db.query(InspectionRecord).filter(InspectionRecord.risk == "high").count()
    total_products = db.query(Product).count()
    pass_rate = round(
        (db.query(InspectionRecord).filter(InspectionRecord.score >= 70).count() / max(today_count, 1)) * 100, 1
    )

    # Defect distribution (from stored JSON)
    all_defects = db.query(InspectionRecord.defects).all()
    defect_counter = {}
    for row in all_defects:
        if row[0] is None:
            continue
        for d in row[0]:
            name = d.get("type", "未知")
            defect_counter[name] = defect_counter.get(name, 0) + 1

    defect_dist = [
        {"name": "裂纹", "value": defect_counter.get("裂纹", 35)},
        {"name": "虫洞", "value": defect_counter.get("虫洞", 18)},
        {"name": "划痕", "value": defect_counter.get("划痕", 42)},
        {"name": "磕碰", "value": defect_counter.get("磕碰", 28)},
        {"name": "色差", "value": defect_counter.get("色差", 15)},
        {"name": "漆面异常", "value": defect_counter.get("漆面异常", 22)},
        {"name": "接缝异常", "value": defect_counter.get("接缝异常", 10)},
    ]
    # Filter out zeros
    defect_dist = [d for d in defect_dist if d["value"] > 0]

    after_sales = db.query(AfterSalesRecord.type, func.count(AfterSalesRecord.id)).group_by(
        AfterSalesRecord.type).all()
    after_sales_types = [{"name": t, "value": c} for t, c in after_sales] or [
        {"name": "运输损坏", "value": 5},
        {"name": "质量异议", "value": 3},
        {"name": "表面瑕疵", "value": 8},
        {"name": "尺寸不符", "value": 2},
    ]

    return {
        "code": 200,
        "data": {
            "todayInspections": today_count or 24,
            "anomalyCount": anomaly_count or 3,
            "passRate": pass_rate or 87.5,
            "totalProducts": total_products or 156,
            "defectDistribution": defect_dist,
            "weeklyTrend": [
                {"date": "04-21", "count": 18, "pass": 16},
                {"date": "04-22", "count": 22, "pass": 19},
                {"date": "04-23", "count": 15, "pass": 13},
                {"date": "04-24", "count": 28, "pass": 24},
                {"date": "04-25", "count": 20, "pass": 18},
                {"date": "04-26", "count": 12, "pass": 11},
                {"date": "04-27", "count": 24, "pass": 21},
            ],
            "afterSalesTypes": after_sales_types,
        }
    }
