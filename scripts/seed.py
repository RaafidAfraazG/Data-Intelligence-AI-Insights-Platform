"""
scripts/seed.py
===============
Seed script to populate the PostgreSQL database with realistic sample data.
Reads from data/products_sample.csv and data/reviews_sample.csv.
"""

import csv
import logging
from pathlib import Path
from datetime import datetime

from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.models.product import Product
from app.models.review import Review

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PRODUCTS_CSV = DATA_DIR / "products_sample.csv"
REVIEWS_CSV = DATA_DIR / "reviews_sample.csv"

def seed_database():
    """Seed the database with sample products and reviews."""
    logger.info("Starting database seed process...")
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if we already have data
        existing_products = db.query(Product).count()
        if existing_products > 0:
            logger.warning(f"Database already contains {existing_products} products. Clearing existing data...")
            # Using SQLAlchemy cascade deletes, deleting products will delete reviews
            db.query(Product).delete()
            db.commit()
            
        logger.info(f"Reading products from {PRODUCTS_CSV}")
        if not PRODUCTS_CSV.exists():
            logger.error(f"Products CSV not found at {PRODUCTS_CSV}")
            return
            
        # 1. Seed Products
        products_inserted = 0
        product_id_map = {} # Map CSV ID to DB ID
        
        with open(PRODUCTS_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    product = Product(
                        name=row["name"],
                        brand=row.get("brand"),
                        category=row.get("category"),
                        price=float(row["price"]) if row.get("price") else None,
                        rating=float(row["rating"]) if row.get("rating") else None,
                        review_count=int(row["review_count"]) if row.get("review_count") else None,
                        description=row.get("description"),
                        source=row.get("source")
                    )
                    db.add(product)
                    db.flush() # To get the ID
                    product_id_map[row["id"]] = product.id
                    products_inserted += 1
                except Exception as e:
                    logger.error(f"Error inserting product {row.get('name')}: {e}")
                    
        logger.info(f"Inserted {products_inserted} products.")
        
        # 2. Seed Reviews
        logger.info(f"Reading reviews from {REVIEWS_CSV}")
        if not REVIEWS_CSV.exists():
            logger.error(f"Reviews CSV not found at {REVIEWS_CSV}")
            return
            
        reviews_inserted = 0
        with open(REVIEWS_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    csv_product_id = row["product_id"]
                    db_product_id = product_id_map.get(csv_product_id)
                    
                    if not db_product_id:
                        logger.warning(f"Product ID {csv_product_id} not found for review. Skipping.")
                        continue
                        
                    review = Review(
                        product_id=db_product_id,
                        reviewer=row.get("reviewer"),
                        rating=float(row["rating"]) if row.get("rating") else None,
                        review_text=row.get("review_text"),
                        review_date=datetime.strptime(row["review_date"], "%Y-%m-%d").date() if row.get("review_date") else None
                    )
                    db.add(review)
                    reviews_inserted += 1
                except Exception as e:
                    logger.error(f"Error inserting review: {e}")
                    
        db.commit()
        logger.info(f"Inserted {reviews_inserted} reviews.")
        logger.info("Database seeding completed successfully! 🎉")
        
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
