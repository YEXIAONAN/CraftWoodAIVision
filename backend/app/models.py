"""CraftWoodAIVision Backend — SQLAlchemy Models"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime,
    ForeignKey, JSON,
)
from sqlalchemy.orm import relationship
from app.database import Base


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    name = Column(String(64), nullable=False)
    role = Column(String(32), default="admin")
    avatar = Column(String(256), default="")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=_now)


class Product(Base):
    __tablename__ = "product"

    id = Column(String(32), primary_key=True)
    name = Column(String(128), nullable=False)
    type = Column(String(64), default="红木家具")
    dimensions = Column(String(128), default="")
    material = Column(String(64), default="")
    batch = Column(String(64), default="")
    status = Column(String(32), default="已入库")
    grade = Column(String(16), default="A级")
    inspector = Column(String(64), default="")
    image = Column(String(256), default="")
    date = Column(String(32), default="")
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now, onupdate=_now)


class InspectionRecord(Base):
    __tablename__ = "inspection_record"

    id = Column(String(32), primary_key=True)
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), default="")
    date = Column(String(32), default="")
    inspector = Column(String(64), default="")
    scene = Column(String(32), default="入库检测")
    risk = Column(String(16), default="low")
    risk_label = Column(String(16), default="低风险")
    score = Column(Float, default=0.0)
    defects = Column(JSON, default=list)
    image = Column(String(256), default="")
    annotated_image = Column(String(256), default="")
    notes = Column(Text, default="")
    reviewed = Column(Integer, default=0)
    created_at = Column(DateTime, default=_now)


class WarehouseRecord(Base):
    __tablename__ = "warehouse_record"

    id = Column(String(32), primary_key=True)
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), default="")
    action = Column(String(32), nullable=False)
    operator = Column(String(64), default="")
    date = Column(String(32), default="")
    notes = Column(Text, default="")
    status = Column(String(32), default="已完成")
    created_at = Column(DateTime, default=_now)


class ReportRecord(Base):
    __tablename__ = "report_record"

    id = Column(String(32), primary_key=True)
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), default="")
    date = Column(String(32), default="")
    inspector = Column(String(64), default="")
    conclusion = Column(String(32), default="合格")
    risk = Column(String(16), default="低风险")
    score = Column(Float, default=0.0)
    file_path = Column(String(256), default="")
    created_at = Column(DateTime, default=_now)


class TraceRecord(Base):
    __tablename__ = "trace_record"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    access_time = Column(DateTime, default=_now)
    access_source = Column(String(64), default="")
    access_content = Column(String(256), default="")


class AfterSalesRecord(Base):
    __tablename__ = "after_sales_record"

    id = Column(String(32), primary_key=True)
    product_id = Column(String(32), ForeignKey("product.id"), nullable=False)
    product_name = Column(String(128), default="")
    type = Column(String(32), nullable=False)
    description = Column(Text, default="")
    status = Column(String(32), default="待处理")
    customer = Column(String(64), default="")
    date = Column(String(32), default="")
    handler = Column(String(64), default="")
    created_at = Column(DateTime, default=_now)
