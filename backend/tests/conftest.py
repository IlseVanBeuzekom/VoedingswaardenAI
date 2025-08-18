import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.product import Base
from repositories.product_repository import ProductRepository
from services.product_service import ProductService


@pytest.fixture
def test_db():
    """Create in-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def product_repo(test_db):
    """Product repository fixture"""
    return ProductRepository(test_db)


@pytest.fixture
def product_service(product_repo):
    """Product service fixture"""
    return ProductService(product_repo)


@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "name": "Test Product",
        "serving_size": 100.0,
        "serving_unit": "gram",
        "serving_amount": 100.0,
        "energy_kcal": 250.0,
        "fats": 10.0,
        "carbohydrates": 30.0,
        "sugars": 15.0,
        "fibers": 5.0,
        "proteins": 20.0
    }


@pytest.fixture
def minimal_product_data():
    """Minimal product data without optional fields"""
    return {
        "name": "Minimal Product",
        "serving_size": 50.0,
        "energy_kcal": 150.0,
        "fats": 5.0,
        "carbohydrates": 20.0,
        "sugars": 10.0,
        "fibers": 3.0,
        "proteins": 12.0
    }
