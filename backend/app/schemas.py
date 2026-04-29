"""CraftWoodAIVision Backend — Pydantic Schemas"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


# ---- Common ----
class MessageResponse(BaseModel):
    code: int = 200
    message: str = "ok"


class PaginatedResponse(BaseModel):
    code: int = 200
    data: dict


# ---- Auth ----
class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    name: str
    role: str
    avatar: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    code: int = 200
    token: str
    user: UserOut


# ---- Product ----
class ProductOut(BaseModel):
    id: str
    name: str
    type: str
    dimensions: str
    material: str
    batch: str
    status: str
    inspector: str
    date: str
    image: str
    grade: str

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    type: str = "红木家具"
    material: str = ""
    dimensions: str = ""
    batch: str = ""
    inspector: str = ""


class ProductListData(BaseModel):
    list: list[ProductOut]
    total: int


# ---- Inspection ----
class DefectItem(BaseModel):
    type: str
    confidence: float
    bbox: list[int]
    area: int


class InspectionOut(BaseModel):
    id: str
    productId: str = Field(alias="product_id")
    productName: str = Field(alias="product_name")
    date: str
    inspector: str
    scene: str
    risk: str
    riskLabel: str = Field(alias="risk_label")
    score: float
    defects: list[DefectItem]
    image: str
    annotatedImage: str = Field(alias="annotated_image")
    notes: str
    reviewed: int

    class Config:
        from_attributes = True
        populate_by_name = True


class InspectionSubmit(BaseModel):
    scene: str = "入库检测"
    productId: str = ""
    image: str = ""


# ---- Warehouse ----
class WarehouseOut(BaseModel):
    id: str
    productId: str = Field(alias="product_id")
    productName: str = Field(alias="product_name")
    action: str
    operator: str
    date: str
    notes: str
    status: str

    class Config:
        from_attributes = True
        populate_by_name = True


class WarehouseCreate(BaseModel):
    product_id: str
    product_name: str = ""
    action: str = "入库"
    notes: str = ""


class WarehouseUpdate(BaseModel):
    action: Optional[str] = None
    operator: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None


# ---- Report ----
class ReportOut(BaseModel):
    id: str
    productId: str = Field(alias="product_id")
    productName: str = Field(alias="product_name")
    date: str
    inspector: str
    conclusion: str
    risk: str
    score: float

    class Config:
        from_attributes = True
        populate_by_name = True


class ReportCreate(BaseModel):
    product_id: str
    product_name: str = ""
    inspector: str = ""
    conclusion: str = "合格"
    risk: str = "低风险"
    score: float = 0.0


class ReportUpdate(BaseModel):
    conclusion: Optional[str] = None
    risk: Optional[str] = None
    score: Optional[float] = None
    inspector: Optional[str] = None


# ---- After-Sales ----
class AfterSalesOut(BaseModel):
    id: str
    productId: str = Field(alias="product_id")
    productName: str = Field(alias="product_name")
    type: str
    description: str
    status: str
    customer: str
    date: str
    handler: str

    class Config:
        from_attributes = True
        populate_by_name = True


class AfterSalesCreate(BaseModel):
    product_id: str
    product_name: str = ""
    type: str = "运输损坏"
    description: str = ""
    customer: str = ""


class AfterSalesUpdate(BaseModel):
    handler: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None


# ---- Dashboard ----
class DefectDistItem(BaseModel):
    name: str
    value: int


class TrendItem(BaseModel):
    date: str
    count: int
    pass_: int = Field(alias="pass")


class AfterSalesTypeItem(BaseModel):
    name: str
    value: int


class DashboardStats(BaseModel):
    todayInspections: int
    anomalyCount: int
    passRate: float
    totalProducts: int
    defectDistribution: list[DefectDistItem]
    weeklyTrend: list[TrendItem]
    afterSalesTypes: list[AfterSalesTypeItem]


# ---- Trace ----
class TraceInspection(BaseModel):
    scene: str
    date: str
    result: str
    risk: str


class TraceOut(BaseModel):
    productId: str
    name: str
    material: str
    dimensions: str
    batch: str
    grade: str
    inspections: list[TraceInspection]
    reportUrl: str
    maintainTips: str
