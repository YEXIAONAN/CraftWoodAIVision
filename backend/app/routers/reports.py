"""CraftWoodAIVision Backend — Reports Router"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.database import get_db
from app.models import ReportRecord, InspectionRecord, Product, User
from app.schemas import ReportOut, ReportCreate, ReportUpdate
from app.deps import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _now_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _generate_report_pdf(report: ReportRecord, product: Product | None, inspections: list[InspectionRecord]) -> io.BytesIO:
    """Generate a plain text report as PDF-alike (text/plain for simplicity; swap with fpdf2/weasyprint in production)."""
    buf = io.BytesIO()
    lines = [
        "=" * 60,
        "     匠木云检 — 产品质量检测报告",
        "=" * 60,
        "",
        f"  报告编号：{report.id}",
        f"  生成日期：{report.date}",
        f"  产品编号：{report.product_id}",
        f"  产品名称：{report.product_name}",
        f"  检测人员：{report.inspector}",
        f"  质检结论：{report.conclusion}",
        f"  风险等级：{report.risk}",
        f"  质检评分：{report.score}",
        "",
    ]
    if product:
        lines += [
            "  --- 产品信息 ---",
            f"  材质：{product.material}",
            f"  规格：{product.dimensions}",
            f"  批次：{product.batch}",
            f"  等级：{product.grade}",
            "",
        ]
    if inspections:
        lines.append("  --- 关联检测记录 ---")
        for ins in inspections:
            lines.append(f"  {ins.id} | {ins.scene} | {ins.date} | 风险:{ins.risk_label} | 评分:{ins.score}")
        lines.append("")

    lines += [
        "",
        "  本报告基于 AI 视觉检测模型生成，结合人工复核确认。",
        "  检测结果仅反映本次送检产品表面质量状况。",
        "-" * 60,
        f"  生成时间：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
    ]
    buf.write("\n".join(lines).encode("utf-8"))
    buf.seek(0)
    return buf


@router.get("")
def list_reports(
    keyword: str = Query("", max_length=64),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(ReportRecord)
    if keyword:
        q = q.filter(
            (ReportRecord.product_name.contains(keyword)) |
            (ReportRecord.product_id.contains(keyword))
        )
    total = q.count()
    items = q.order_by(ReportRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "code": 200,
        "data": {
            "list": [ReportOut.model_validate(r) for r in items],
            "total": total,
            "page": page,
            "pageSize": page_size,
        }
    }


@router.get("/{report_id}")
def get_report(report_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rpt = db.query(ReportRecord).filter(ReportRecord.id == report_id).first()
    if not rpt:
        return {"code": 404, "message": "报告不存在", "data": None}
    product = db.query(Product).filter(Product.id == rpt.product_id).first()
    inspections = db.query(InspectionRecord).filter(InspectionRecord.product_id == rpt.product_id).all()
    result = ReportOut.model_validate(rpt).model_dump()
    if product:
        result["product"] = {
            "material": product.material,
            "dimensions": product.dimensions,
            "batch": product.batch,
            "grade": product.grade,
        }
    result["inspections"] = [
        {"id": i.id, "scene": i.scene, "date": i.date, "risk": i.risk_label, "score": i.score}
        for i in inspections
    ]
    return {"code": 200, "data": result}


@router.post("")
def create_report(data: ReportCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    count = db.query(ReportRecord).count()
    rpt = ReportRecord(
        id=f"RPT-{count + 1:04d}",
        product_id=data.product_id,
        product_name=data.product_name,
        date=_now_str(),
        inspector=data.inspector or user.name,
        conclusion=data.conclusion,
        risk=data.risk,
        score=data.score,
    )
    db.add(rpt)
    db.commit()
    db.refresh(rpt)
    return {"code": 200, "data": ReportOut.model_validate(rpt), "message": "报告创建成功"}


@router.put("/{report_id}")
def update_report(report_id: str, data: ReportUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rpt = db.query(ReportRecord).filter(ReportRecord.id == report_id).first()
    if not rpt:
        return {"code": 404, "message": "报告不存在", "data": None}
    updates = data.model_dump(exclude_unset=True)
    for k, v in updates.items():
        setattr(rpt, k, v)
    db.commit()
    db.refresh(rpt)
    return {"code": 200, "data": ReportOut.model_validate(rpt), "message": "更新成功"}


@router.delete("/{report_id}")
def delete_report(report_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rpt = db.query(ReportRecord).filter(ReportRecord.id == report_id).first()
    if not rpt:
        return {"code": 404, "message": "报告不存在", "data": None}
    db.delete(rpt)
    db.commit()
    return {"code": 200, "message": "删除成功"}


@router.get("/{report_id}/download")
def download_report(report_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rpt = db.query(ReportRecord).filter(ReportRecord.id == report_id).first()
    if not rpt:
        return {"code": 404, "message": "报告不存在"}
    product = db.query(Product).filter(Product.id == rpt.product_id).first()
    inspections = db.query(InspectionRecord).filter(InspectionRecord.product_id == rpt.product_id).all()
    buf = _generate_report_pdf(rpt, product, inspections)
    return StreamingResponse(
        buf,
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={report_id}_report.txt"}
    )
