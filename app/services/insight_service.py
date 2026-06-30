"""
app/services/insight_service.py
==================================
AI-powered market intelligence insight generation using Gemini.

Each method focuses on one type of insight and uses a carefully crafted
prompt template. All prompts are stored inline for simplicity.
"""

import logging

from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.repositories.review import ReviewRepository
from app.nlp.sentiment import product_sentiment_summary
from app.nlp.keywords import extract_keywords
from app.config.settings import settings

logger = logging.getLogger(__name__)


def _call_gemini(prompt: str, fallback: str = "Insight unavailable.") -> str:
    """Shared Gemini caller with graceful fallback."""
    if not settings.GEMINI_API_KEY:
        return fallback + " (GEMINI_API_KEY not set)"
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        logger.error("Gemini insight call failed: %s", exc)
        return fallback


def _product_snapshot(product, reviews: list) -> str:
    """Format a product + its reviews into a readable block for Gemini prompts."""
    review_texts = [r.review_text for r in reviews if r.review_text]
    sample = " | ".join(review_texts[:8]) or "No reviews."
    return (
        f"Product: {product.name} | Brand: {product.brand or 'N/A'} | "
        f"Category: {product.category or 'N/A'} | Price: {product.price or 'N/A'} | "
        f"Rating: {product.rating or 'N/A'}/5 ({product.review_count or 0} reviews)\n"
        f"Reviews: {sample}"
    )


class InsightService:
    """
    Generates structured AI insights about products using Gemini.
    Each method is independently callable for flexible use.
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        self.product_repo = ProductRepository(db)
        self.review_repo = ReviewRepository(db)

    # ── Product-level insights ────────────────────────────────────────────────

    def generate_product_strengths(self, product_id: int) -> str:
        """Identify what customers love most about a product."""
        logger.info("Generating product strengths for product_id=%d", product_id)
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning("Product ID %d not found.", product_id)
            return "Product not found."
        reviews = self.review_repo.get_by_product(product_id)
        snapshot = _product_snapshot(product, reviews)

        prompt = f"""Based on the following product data, list the top 3–5 STRENGTHS of this product.
Focus on what customers praise. Be specific and concise.

{snapshot}

Format: A numbered list of strengths."""
        return _call_gemini(prompt)

    def generate_product_weaknesses(self, product_id: int) -> str:
        """Identify common complaints and weaknesses."""
        logger.info("Generating product weaknesses for product_id=%d", product_id)
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning("Product ID %d not found.", product_id)
            return "Product not found."
        reviews = self.review_repo.get_by_product(product_id)
        snapshot = _product_snapshot(product, reviews)

        prompt = f"""Based on the following product data, list the top 3–5 WEAKNESSES or complaints.
Focus on what customers dislike. Be specific and honest.

{snapshot}

Format: A numbered list of weaknesses."""
        return _call_gemini(prompt)

    def generate_pain_points(self, product_id: int) -> str:
        """Extract the most frustrating customer experiences."""
        logger.info("Generating pain points for product_id=%d", product_id)
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning("Product ID %d not found.", product_id)
            return "Product not found."
        reviews = self.review_repo.get_by_product(product_id)
        review_texts = [r.review_text for r in reviews if r.review_text]

        if not review_texts:
            return "No reviews available to extract pain points."

        combined = "\n".join(f"- {t}" for t in review_texts[:15])
        prompt = f"""Analyze these customer reviews for {product.name} and identify the 
TOP CUSTOMER PAIN POINTS — the most frustrating or frequently complained-about issues.

Reviews:
{combined}

List 3–5 specific pain points with a brief explanation of each."""
        return _call_gemini(prompt)

    def generate_marketing_recommendations(self, product_id: int) -> str:
        """Suggest marketing copy and positioning strategies."""
        logger.info("Generating marketing recommendations for product_id=%d", product_id)
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning("Product ID %d not found.", product_id)
            return "Product not found."
        reviews = self.review_repo.get_by_product(product_id)
        snapshot = _product_snapshot(product, reviews)

        prompt = f"""You are a digital marketing strategist. Based on this product's data, provide 
3–5 actionable marketing recommendations.

{snapshot}

Include suggestions for: target audience, key selling points to highlight,
and one suggested ad headline. Keep it concise."""
        return _call_gemini(prompt)

    def generate_seo_keywords(self, product_id: int) -> list[str]:
        """Extract SEO-friendly keywords from product data and reviews."""
        product = self.product_repo.get(product_id)
        if not product:
            return []
        reviews = self.review_repo.get_by_product(product_id)

        texts = []
        if product.name:
            texts.append(product.name)
        if product.description:
            texts.append(product.description)
        for r in reviews:
            if r.review_text:
                texts.append(r.review_text)

        keywords = extract_keywords(texts, top_n=15)
        return [k["keyword"] for k in keywords]

    # ── Multi-product insights ─────────────────────────────────────────────────

    def generate_competitor_comparison(self, product_ids: list[int]) -> str:
        """Compare multiple products as competitors."""
        logger.info("Generating competitor comparison for product_ids=%s", product_ids)
        products = [self.product_repo.get(pid) for pid in product_ids]
        products = [p for p in products if p]

        if len(products) < 2:
            logger.warning("Not enough valid products found for comparison.")
            return "Need at least 2 valid products for comparison."

        blocks = []
        for p in products[:5]:  # Limit to 5 to keep prompt manageable
            reviews = self.review_repo.get_by_product(p.id)
            blocks.append(_product_snapshot(p, reviews))

        combined = "\n\n".join(f"Competitor {i+1}:\n{b}" for i, b in enumerate(blocks))

        prompt = f"""You are a market intelligence analyst. Compare the following competing products.

{combined}

Provide a structured analysis covering:
1. Price positioning
2. Customer satisfaction ranking
3. Key differentiators
4. Market positioning recommendation

Keep the response to 5–8 sentences or a concise bullet list."""
        return _call_gemini(prompt)

    def generate_executive_summary(self, product_ids: list[int]) -> str:
        """Generate a board-level executive summary of the dataset."""
        logger.info("Generating executive summary for %d products", len(product_ids))
        total_products = len(product_ids)
        products = [self.product_repo.get(pid) for pid in product_ids[:10]]
        products = [p for p in products if p]

        all_review_texts = []
        for p in products:
            reviews = self.review_repo.get_by_product(p.id)
            all_review_texts.extend(r.review_text for r in reviews if r.review_text)

        sentiment = product_sentiment_summary(all_review_texts[:100])
        keywords = extract_keywords(all_review_texts[:100], top_n=10)
        keyword_str = ", ".join(k["keyword"] for k in keywords)

        product_names = ", ".join(p.name for p in products[:5])

        prompt = f"""You are a senior market analyst. Write a concise executive summary for a 
market intelligence report based on the following dataset:

Total Products Analysed: {total_products}
Sample Products: {product_names}
Overall Customer Sentiment: {sentiment['overall_label']} (score: {sentiment['average_score']})
Sentiment Distribution: {sentiment['distribution']}
Top Keywords: {keyword_str}

Write a professional 3–4 sentence executive summary suitable for a business stakeholder.
Highlight key market trends, customer sentiment, and a strategic recommendation."""
        return _call_gemini(prompt)
