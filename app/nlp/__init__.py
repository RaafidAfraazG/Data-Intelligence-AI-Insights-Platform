"""
app/nlp/__init__.py
NLP package — exposes submodules for convenient imports.
"""
from app.nlp import preprocessor, sentiment, keywords, topics, summarizer

__all__ = ["preprocessor", "sentiment", "keywords", "topics", "summarizer"]
