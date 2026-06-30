"""
tests/test_cleaner.py
======================
Unit tests for data-cleaning utility functions.
These are pure function tests — no database or HTTP involved.
"""

import pandas as pd
from app.preprocessing.cleaner import (
    normalize_price,
    clean_html,
    normalize_text,
    remove_special_characters,
    standardize_categories,
    remove_duplicates,
)


# ── normalize_price ───────────────────────────────────────────────────────────

def test_normalize_price_string_with_dollar():
    assert normalize_price("$12.99") == 12.99

def test_normalize_price_string_with_comma():
    assert normalize_price("1,299.00") == 1299.0

def test_normalize_price_numeric():
    assert normalize_price(49) == 49.0

def test_normalize_price_none():
    assert normalize_price(None) is None

def test_normalize_price_invalid():
    assert normalize_price("not-a-price") is None


# ── clean_html ────────────────────────────────────────────────────────────────

def test_clean_html_removes_tags():
    assert clean_html("<p>Hello <b>world</b></p>") == "Hello world"

def test_clean_html_empty():
    assert clean_html("") == ""

def test_clean_html_plain_text():
    assert clean_html("No tags here") == "No tags here"


# ── normalize_text ────────────────────────────────────────────────────────────

def test_normalize_text_lowercases():
    assert normalize_text("APPLE iPhone 15") == "apple iphone 15"

def test_normalize_text_trims():
    assert normalize_text("  hello  ") == "hello"

def test_normalize_text_collapses_spaces():
    assert normalize_text("too   many   spaces") == "too many spaces"


# ── remove_special_characters ─────────────────────────────────────────────────

def test_remove_special_characters_basic():
    result = remove_special_characters("Hello, World! #2")
    assert "," not in result
    assert "!" not in result
    assert "#" not in result

def test_remove_special_characters_keeps_spaces():
    result = remove_special_characters("Hello World")
    assert "Hello" in result and "World" in result


# ── standardize_categories ────────────────────────────────────────────────────

def test_standardize_known_category():
    assert standardize_categories("Electronics") == "electronics"

def test_standardize_unknown_category():
    assert standardize_categories("Unicorn Products") == "other"

def test_standardize_none():
    assert standardize_categories(None) == "other"


# ── remove_duplicates ─────────────────────────────────────────────────────────

def test_remove_duplicates_exact():
    df = pd.DataFrame([
        {"name": "Widget A", "price": 10},
        {"name": "Widget A", "price": 10},
        {"name": "Widget B", "price": 20},
    ])
    result = remove_duplicates(df)
    assert len(result) == 2
