"""
tests/test_nlp.py
=================
Tests for the NLP module including sentiment analysis,
keyword extraction, and topic modeling.
"""

from app.nlp.sentiment import product_sentiment_summary, _analyze_vader
from app.nlp.keywords import extract_keywords
from app.nlp.topics import extract_topics


def test_vader_sentiment():
    """Test basic VADER sentiment scoring."""
    positive = _analyze_vader("I absolutely love this phone, it is amazing!")
    assert positive["compound"] > 0.5
    assert positive["label"] == "Positive"

    negative = _analyze_vader("Terrible experience. The battery dies in 2 hours and customer service is rude.")
    assert negative["compound"] < -0.5
    assert negative["label"] == "Negative"

    neutral = _analyze_vader("The phone has a 6-inch screen and comes in black.")
    assert neutral["label"] == "Neutral"


def test_product_sentiment_summary():
    """Test the aggregation of sentiment across multiple reviews."""
    reviews = [
        "Great product, highly recommend!",
        "It's okay, nothing special.",
        "Worst purchase ever. Broke immediately.",
        "Very good quality for the price.",
    ]
    summary = product_sentiment_summary(reviews)

    assert "average_score" in summary
    assert "overall_label" in summary
    assert "distribution" in summary
    assert summary["distribution"]["Positive"] >= 2
    assert summary["distribution"]["Negative"] >= 1
    assert summary["distribution"]["Neutral"] >= 0


def test_extract_keywords():
    """Test TF-IDF keyword extraction."""
    texts = [
        "The battery life on this laptop is incredible. I can work all day without charging.",
        "Amazing battery, highly recommended for travel.",
        "Terrible battery performance. It drains too fast.",
    ]
    keywords = extract_keywords(texts, top_n=3)

    assert len(keywords) == 3
    # 'battery' should definitely be a top keyword
    keyword_strings = [k["keyword"] for k in keywords]
    assert any("battery" in k.lower() for k in keyword_strings)


def test_extract_topics():
    """Test LDA topic modeling."""
    texts = [
        "The screen quality is amazing, very bright display.",
        "Colors on the display are vivid and punchy.",
        "Customer service was terrible when I called.",
        "Support team was unhelpful and rude.",
    ]
    # We expect 2 topics: one about screen/display, one about service/support
    topics = extract_topics(texts, n_topics=2, num_words=3)

    assert len(topics) == 2
    assert len(topics[0]["words"]) == 3
