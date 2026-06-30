"""
app/utils/report_builder.py
============================
Assembles a Markdown market intelligence report from structured data.

Keeps all string formatting in one place — agents just supply the data.
"""

from datetime import datetime, timezone
from typing import Any


class ReportBuilder:
    """Builds a formatted Markdown string from analysis results."""

    def build_report(
        self,
        stats: dict[str, Any],
        products: list[dict[str, Any]],
        sentiment: dict[str, Any],
        keywords: list[dict[str, Any]],
        topics: list[dict[str, Any]],
        executive_summary: str,
    ) -> str:
        """
        Assemble all sections into a single Markdown string.

        Parameters
        ----------
        stats : dict         — dataset statistics
        products : list      — top product records
        sentiment : dict     — sentiment summary from sentiment.py
        keywords : list      — keyword dicts from keywords.py
        topics : list        — topic dicts from topics.py
        executive_summary : str — Gemini-generated executive summary

        Returns
        -------
        str — complete Markdown document
        """
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        sections = [
            self._header(now),
            self._executive_summary(executive_summary),
            self._dataset_stats(stats),
            self._top_products(products),
            self._sentiment_section(sentiment),
            self._keywords_section(keywords),
            self._topics_section(topics),
            self._footer(),
        ]
        return "\n\n".join(sections)

    # ── Sections ──────────────────────────────────────────────────────────────

    def _header(self, timestamp: str) -> str:
        return (
            f"# 🧠 AI Market Intelligence Report\n\n"
            f"**Generated:** {timestamp}  \n"
            f"**Platform:** AI Market Intelligence Platform v0.2.0"
        )

    def _executive_summary(self, summary: str) -> str:
        return f"## 📋 Executive Summary\n\n{summary}"

    def _dataset_stats(self, stats: dict) -> str:
        lines = [
            "## 📊 Dataset Statistics\n",
            "| Metric | Value |",
            "|---|---|",
            f"| Total Products in Database | {stats.get('total_products', 'N/A')} |",
            f"| Products in This Report | {stats.get('products_in_report', 'N/A')} |",
            f"| Reviews Analysed | {stats.get('reviews_analysed', 'N/A')} |",
        ]
        return "\n".join(lines)

    def _top_products(self, products: list[dict]) -> str:
        if not products:
            return "## 🛒 Top Products\n\n_No products available._"

        rows = [
            "## 🛒 Top Products\n",
            "| # | Name | Brand | Category | Price | Rating |",
            "|---|---|---|---|---|---|",
        ]
        for i, p in enumerate(products, 1):
            name = (p.get("name") or "N/A")[:40]
            brand = p.get("brand") or "N/A"
            cat = p.get("category") or "N/A"
            price = f"₹{p['price']:,.0f}" if p.get("price") else "N/A"
            rating = f"{p['rating']}/5" if p.get("rating") else "N/A"
            rows.append(f"| {i} | {name} | {brand} | {cat} | {price} | {rating} |")
        return "\n".join(rows)

    def _sentiment_section(self, sentiment: dict) -> str:
        dist = sentiment.get("distribution", {})
        avg = sentiment.get("average_score", 0)
        label = sentiment.get("overall_label", "neutral")
        total = sentiment.get("total_reviews", 0)

        pos = dist.get("positive", 0)
        neu = dist.get("neutral", 0)
        neg = dist.get("negative", 0)

        return (
            f"## 😊 Customer Sentiment\n\n"
            f"**Overall Sentiment:** {label.capitalize()}  \n"
            f"**Average Score:** {avg} (range: -1 to 1)  \n"
            f"**Total Reviews Analysed:** {total}\n\n"
            f"| Sentiment | Count | Percentage |\n"
            f"|---|---|---|\n"
            f"| ✅ Positive | {pos} | {_pct(pos, total)} |\n"
            f"| ➖ Neutral  | {neu} | {_pct(neu, total)} |\n"
            f"| ❌ Negative | {neg} | {_pct(neg, total)} |"
        )

    def _keywords_section(self, keywords: list[dict]) -> str:
        if not keywords:
            return "## 🔑 Top Keywords\n\n_No keywords extracted._"

        rows = [
            "## 🔑 Top Keywords\n",
            "| Keyword | TF-IDF Score |",
            "|---|---|",
        ]
        for kw in keywords[:15]:
            rows.append(f"| {kw['keyword']} | {kw['score']} |")
        return "\n".join(rows)

    def _topics_section(self, topics: list[dict]) -> str:
        if not topics:
            return "## 💬 Discussion Topics\n\n_No topics extracted (need more reviews)._"

        lines = ["## 💬 Discussion Topics\n"]
        for t in topics:
            words = ", ".join(t.get("words", []))
            lines.append(f"**Topic {t['topic_id']}:** {words}")
        return "\n".join(lines)

    def _footer(self) -> str:
        return (
            "---\n\n"
            "_This report was automatically generated by the AI Market Intelligence Platform._  \n"
            "_Powered by VADER Sentiment, TF-IDF, LDA, and Google Gemini._"
        )


def _pct(count: int, total: int) -> str:
    if total == 0:
        return "0%"
    return f"{round(count / total * 100, 1)}%"
