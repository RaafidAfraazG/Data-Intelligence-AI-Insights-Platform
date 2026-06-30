"""
app/agents/report_generator_agent.py
=======================================
ReportGeneratorAgent — generates a Markdown market intelligence report.

Pipeline:
  1. Run InsightGeneratorAgent to get all NLP + AI data
  2. Fetch product stats from PostgreSQL
  3. Use ReportBuilder to assemble the Markdown
  4. Save to reports/report_TIMESTAMP.md
  5. Return the file path
"""

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.agents.insight_generator_agent import InsightGeneratorAgent
from app.repositories.product import ProductRepository
from app.utils.report_builder import ReportBuilder
from app.utils.helpers import build_export_filename

logger = logging.getLogger(__name__)


class ReportGeneratorAgent:
    """
    Coordinates the full reporting pipeline:
    data → NLP → AI insights → Markdown report file.
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        self.product_repo = ProductRepository(db)
        self.insight_agent = InsightGeneratorAgent(db)

    def run(self, product_ids: list[int] | None = None) -> dict[str, Any]:
        """
        Generate a complete Markdown report and save it to disk.

        Parameters
        ----------
        product_ids : list[int] | None
            IDs of products to include. If None, uses all products (max 50).

        Returns
        -------
        dict: { file_path, products_included, report_preview (first 300 chars) }
        """
        logger.info("ReportGeneratorAgent starting.")

        # ── Resolve product IDs ───────────────────────────────────────────────
        if not product_ids:
            all_products = self.product_repo.get_all(skip=0, limit=50)
            product_ids = [p.id for p in all_products]

        if not product_ids:
            return {"error": "No products found in the database.", "file_path": None}

        # ── Run insight pipeline ──────────────────────────────────────────────
        insights = self.insight_agent.run(product_ids)

        # ── Gather top products for the report ────────────────────────────────
        top_products = []
        for pid in product_ids[:10]:
            p = self.product_repo.get(pid)
            if p:
                top_products.append({
                    "id": p.id,
                    "name": p.name,
                    "brand": p.brand,
                    "category": p.category,
                    "price": p.price,
                    "rating": p.rating,
                    "review_count": p.review_count,
                })

        # ── Dataset stats ─────────────────────────────────────────────────────
        stats = {
            "total_products": self.product_repo.count(),
            "products_in_report": len(product_ids),
            "reviews_analysed": insights["reviews_analysed"],
        }

        # ── Build Markdown ────────────────────────────────────────────────────
        builder = ReportBuilder()
        markdown = builder.build_report(
            stats=stats,
            products=top_products,
            sentiment=insights["sentiment_summary"],
            keywords=insights["top_keywords"],
            topics=insights["topics"],
            executive_summary=insights["executive_summary"],
        )

        # ── Save to disk ──────────────────────────────────────────────────────
        file_path = build_export_filename("report", "md").replace("exports", "reports")
        import os
        os.makedirs("reports", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        logger.info("Report saved to: %s", file_path)

        return {
            "file_path": file_path,
            "products_included": len(product_ids),
            "report_preview": markdown[:300] + "...",
        }
