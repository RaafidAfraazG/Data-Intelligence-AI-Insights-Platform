"""
app/api/routes/agents.py
=========================
Agent trigger endpoints — kick off multi-step AI pipelines via HTTP.

POST /api/v1/agents/collect   — run DataCollectorAgent
POST /api/v1/agents/insights  — run InsightGeneratorAgent
POST /api/v1/agents/report    — run ReportGeneratorAgent (returns file path)
"""

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.agents.data_collector_agent import DataCollectorAgent
from app.agents.insight_generator_agent import InsightGeneratorAgent
from app.agents.report_generator_agent import ReportGeneratorAgent
from app.core.response import success_response

router = APIRouter(prefix="/agents")
logger = logging.getLogger(__name__)


# ── Request schemas ───────────────────────────────────────────────────────────

class CollectRequest(BaseModel):
    urls: list[str] = []
    csv_path: str | None = None
    scraper_type: str = "beautifulsoup"


class InsightRequest(BaseModel):
    product_ids: list[int]


class ReportRequest(BaseModel):
    product_ids: list[int] | None = None  # None = use all products


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/collect", summary="Run DataCollectorAgent — scrape URLs and/or import CSV")
def run_collector(payload: CollectRequest, db: Session = Depends(get_db)):
    """
    Trigger a full data collection run.
    Scrapes the provided URLs and/or imports the CSV, then cleans the data.
    """
    agent = DataCollectorAgent(db)
    result = agent.run(
        urls=payload.urls,
        csv_path=payload.csv_path,
        scraper_type=payload.scraper_type,
    )
    return success_response(data=result, message="DataCollectorAgent complete.")


@router.post("/insights", summary="Run InsightGeneratorAgent — NLP + embeddings + AI insights")
def run_insight_agent(payload: InsightRequest, db: Session = Depends(get_db)):
    """
    Run the full AI analysis pipeline for the specified products.
    Generates embeddings, indexes to ChromaDB, and produces AI insights.
    """
    if not payload.product_ids:
        return success_response(
            data={},
            message="No product IDs provided.",
            status_code=400,
        )
    agent = InsightGeneratorAgent(db)
    result = agent.run(payload.product_ids)
    return success_response(data=result, message="InsightGeneratorAgent complete.")


@router.post("/report", summary="Run ReportGeneratorAgent — create Markdown report")
def run_report_agent(payload: ReportRequest, db: Session = Depends(get_db)):
    """
    Generate a full Markdown market intelligence report.
    Saved to the reports/ directory. Returns the file path.
    """
    agent = ReportGeneratorAgent(db)
    result = agent.run(product_ids=payload.product_ids)
    return success_response(data=result, message="Report generated successfully.")
