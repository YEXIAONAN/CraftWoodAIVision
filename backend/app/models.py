"""CraftWoodAIVision Backend — SQLAlchemy Models"""

import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, Date,
    ForeignKey, JSON, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    name = Column(String(64), nullable=False)
    role = Column(String(32), default="admin")  # admin, inspector, sales, consumer
    avatar = Column(String(256), default="")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Product(Base):
    __tablename__ = "product"

    id = Column(String(32), primary_key=True)  # e.g. PROD-0001
    name = Column(String(128), nullable=False)
    type = Column(String(64), default="红木家具")
    dimensions = Column(String(128), default="")
    material = Column(String(64), default="")
    batch = Column(String(64), default="")
    status = Column(String(32), default="已入库")  # 已入库, 仓储中, 待出库, 已出库, 已归档
    grade = Column(String(16), default="A级")
    inspector = Column(String(64), default="")
    image = Column(String(256), default="")
    date = Column(String(32), default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class InspectionRecord(Base):
    __tablename__ = "inspection_record"

    id = Column(String(32), primary_key=True)  # e.g. INS-0001
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), default="")
    date = Column(String(32), default="")
    inspector = Column(String(64), default="")
    scene = Column(String(32), default="入库检测")  # 入库检测, 仓储巡检, 出库复检
    risk = Column(String(16), default="low")  # low, medium, high
    risk_label = Column(String(16), default="低风险")
    score = Column(Float, default=0.0)
    defects = Column(JSON, default=list)  # list of defect objects
    image = Column(String(256), default="")
    annotated_image = Column(String(256), default="")
    notes = Column(Text, default="")
    reviewed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class WarehouseRecord(Base):
    __tablename__ = "warehouse_record"

    id = Column(String(32), primary_key=True)  # e.g. WH-0001
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), default="")
    action = Column(String(32), nullable=False)  # 入库, 仓储巡检, 出库复检, 出库
    operator = Column(String(64), default="")
    date = Column(String(32), default="")
    notes = Column(Text, default="")
    status = Column(String(32), default="已完成")  # 已完成, 待处理
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ReportRecord(Base):
    __tablename__ = "report_record"

    id = Column(String(32), primary_key=True)  # e.g. RPT-0001
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), default="")
    date = Column(String(32), default="")
    inspector = Column(String(64), default="")
    conclusion = Column(String(32), default="合格")  # 合格, 条件合格, 需复检
    risk = Column(String(16), default="低风险")
    score = Column(Float, default=0.0)
    file_path = Column(String(256), default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class TraceRecord(Base):
    __tablename__ = "trace_record"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    access_time = Column(DateTime, default=datetime.datetime.utcnow)
    access_source = Column(String(64), default="")
    access_content = Column(String(256), default="")


class AfterSalesRecord(Base):
    __tablename__ = "after_sales_record"

    id = Column(String(32), primary_key=True)  # e.g. AS-0001
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), default="")
    type = Column(String(32), nullable=False)  # 运输损坏, 质量异议, 表面瑕疵, 尺寸不符
    description = Column(Text, default="")
    status = Column(String(32), default="待处理")  # 待处理, 处理中, 已完成, 已关闭
    customer = Column(String(64), default="")
    date = Column(String(32), default="")
    handler = Column(String(64), default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
