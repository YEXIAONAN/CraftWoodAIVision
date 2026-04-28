"""CraftWoodAIVision Backend — Seed Data"""

import datetime
from sqlalchemy.orm import Session

from app.models import User, Product, InspectionRecord, WarehouseRecord, ReportRecord, AfterSalesRecord
from app.security import hash_password

PRODUCT_TYPES = ["红酸枝木沙发", "鸡翅木餐桌", "大果紫檀书桌", "红木茶台", "花梨木衣柜", "刺猬紫檀床", "黑酸枝办公桌", "红木圈椅"]
MATERIALS = ["老挝大红酸枝", "缅甸鸡翅木", "大果紫檀", "东非黑黄檀"]
STATUSES = ["已入库", "仓储中", "待出库", "已出库", "已归档"]
GRADES = ["A级", "B级", "A级", "A级", "B级", "C级"]
SCENES = ["入库检测", "仓储巡检", "出库复检"]
INSPECTORS = ["张明远", "李思琪", "王建国"]
OPERATORS = ["张明远", "李思琪", "刘强"]
CONCLUSIONS = ["合格", "条件合格", "需复检", "合格"]
AFTER_SALES_TYPES = ["运输损坏", "质量异议", "表面瑕疵", "尺寸不符"]
AFTER_SALES_STATUSES = ["待处理", "处理中", "已完成", "已关闭"]
AFTER_SALES_DESCS = ["运输过程中出现磕碰", "客户反馈表面有细微划痕", "颜色与样品存在差异", "尺寸与订单不符"]
WAREHOUSE_ACTIONS = ["入库", "仓储巡检", "出库复检", "出库"]
WAREHOUSE_NOTES = ["", "外观良好，无异常", "发现轻微划痕，已记录", "包装完整，准予出库"]
DEFECT_TYPES = ["裂纹", "虫洞", "划痕", "磕碰", "色差", "漆面异常", "接缝异常"]


def seed_database(db: Session):
    """Populate the database with initial seed data matching frontend mock."""

    if db.query(User).count() > 0:
        return  # already seeded

    # ---- User ----
    admin = User(
        username="admin",
        hashed_password=hash_password("admin123"),
        name="张明远",
        role="admin",
    )
    db.add(admin)

    # ---- Products ----
    products = []
    for i in range(18):
        p = Product(
            id=f"PROD-{i + 1:04d}",
            name=PRODUCT_TYPES[i % len(PRODUCT_TYPES)],
            type="红木家具",
            dimensions=f"{180 + (i * 7) % 120}0 × {80 + (i * 13) % 60}0 × {40 + (i * 17) % 40}0 mm",
            material=MATERIALS[i % len(MATERIALS)],
            batch=f"2025-BATCH-{(i // 4) + 1}",
            status=STATUSES[i % len(STATUSES)],
            grade=GRADES[i % len(GRADES)],
            inspector="张明远",
            date=f"2026-{(i % 3) + 1:02d}-{10 + (i % 18):02d}",
            image=f"https://picsum.photos/seed/prod{i}/400/300",
        )
        products.append(p)
        db.add(p)
    db.flush()

    # ---- Inspections ----
    inspections = []
    for i in range(12):
        defects = []
        for _ in range(1 + (i % 5)):
            defects.append({
                "type": DEFECT_TYPES[(i + _) % len(DEFECT_TYPES)],
                "confidence": round(0.75 + (i + _) % 24 * 0.01, 2),
                "bbox": [i * 20 % 300, i * 15 % 300, 50 + (i * 7) % 50, 30 + (i * 11) % 30],
                "area": 50 + (i * 37) % 200,
            })
        risk = ["low", "medium", "high"][i % 3]
        ins = InspectionRecord(
            id=f"INS-{i + 1:04d}",
            product_id=f"PROD-{(i % 18) + 1:04d}",
            product_name=PRODUCT_TYPES[(i + 1) % len(PRODUCT_TYPES)],
            date=f"2026-{(i % 3) + 1:02d}-{10 + (i % 18):02d}",
            inspector=INSPECTORS[i % len(INSPECTORS)],
            scene=SCENES[i % len(SCENES)],
            risk=risk,
            risk_label={"low": "低风险", "medium": "中风险", "high": "高风险"}[risk],
            score=round(60 + (i * 13) % 40 + 0.5, 1),
            defects=defects,
            image=f"https://picsum.photos/seed/ins{i}/800/600",
            annotated_image=f"https://picsum.photos/seed/ann{i}/800/600",
            notes="多处缺陷，建议人工复核" if len(defects) > 3 else "",
            reviewed=1 if i % 3 == 0 else 0,
        )
        inspections.append(ins)
        db.add(ins)

    # ---- Warehouse Records ----
    for i in range(10):
        wh = WarehouseRecord(
            id=f"WH-{i + 1:04d}",
            product_id=f"PROD-{(i % 18) + 1:04d}",
            product_name=PRODUCT_TYPES[(i + 2) % len(PRODUCT_TYPES)],
            action=WAREHOUSE_ACTIONS[i % len(WAREHOUSE_ACTIONS)],
            operator=OPERATORS[i % len(OPERATORS)],
            date=f"2026-{(i % 3) + 1:02d}-{10 + (i % 18):02d}",
            notes=WAREHOUSE_NOTES[i % len(WAREHOUSE_NOTES)],
            status=["已完成", "待处理", "已完成", "已完成"][i % 4],
        )
        db.add(wh)

    # ---- Reports ----
    for i in range(8):
        rpt = ReportRecord(
            id=f"RPT-{i + 1:04d}",
            product_id=f"PROD-{(i % 18) + 1:04d}",
            product_name=PRODUCT_TYPES[(i + 3) % len(PRODUCT_TYPES)],
            date=f"2026-{(i % 3) + 1:02d}-{10 + (i % 18):02d}",
            inspector="张明远",
            conclusion=CONCLUSIONS[i % len(CONCLUSIONS)],
            risk=["低风险", "中风险", "高风险"][i % 3],
            score=round(70 + (i * 17) % 30 + 0.3, 1),
        )
        db.add(rpt)

    # ---- After-Sales ----
    for i in range(6):
        as_ = AfterSalesRecord(
            id=f"AS-{i + 1:04d}",
            product_id=f"PROD-{(i % 18) + 1:04d}",
            product_name=PRODUCT_TYPES[(i + 4) % len(PRODUCT_TYPES)],
            type=AFTER_SALES_TYPES[i % len(AFTER_SALES_TYPES)],
            description=AFTER_SALES_DESCS[i % len(AFTER_SALES_DESCS)],
            status=AFTER_SALES_STATUSES[i % len(AFTER_SALES_STATUSES)],
            customer="陈先生",
            date=f"2026-{(i % 3) + 1:02d}-{10 + (i % 18):02d}",
            handler=i < 4 and OPERATORS[i % len(OPERATORS)] or "",
        )
        db.add(as_)

    db.commit()
