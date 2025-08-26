import pytest
import sys
import os
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.product import Base, ProductDB, ProductCreate
from models.recipe import RecipeDB, RecipeIngredientDB, RecipeCreate, RecipeIngredientCreate
from repositories.product_repository import ProductRepository
from repositories.recipe_repository import RecipeRepository
from services.product_service import ProductService
from services.recipe_service import RecipeService
from datetime import date, timedelta

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
def recipe_repo(test_db):
    """Recipe repository fixture"""
    return RecipeRepository(test_db)

@pytest.fixture
def recipe_service(test_db):
    """Recipe service fixture"""
    recipe_repo = RecipeRepository(test_db)
    return RecipeService(recipe_repo)

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

@pytest.fixture
def sample_products(test_db):
    """Create sample products in database for recipe testing"""
    products = []

    # Product 1: Flour
    product1 = ProductDB(
        name="Bloem",
        serving_size=100.0,
        serving_unit='gram',
        serving_amount=100.0,
        energy_kcal=364.0,
        fats=1.0,
        carbohydrates=76.0,
        sugars=0.3,
        fibers=2.7,
        proteins=10.3
    )
    test_db.add(product1)

    # Product 2: Eggs
    product2 = ProductDB(
        name="Eieren",
        serving_size=100.0,
        serving_unit='stuk',
        serving_amount=1.0,
        energy_kcal=155.0,
        fats=11.0,
        carbohydrates=1.1,
        sugars=1.1,
        fibers=0.0,
        proteins=13.0
    )
    test_db.add(product2)

    # Product 3: Milk
    product3 = ProductDB(
        name="Melk",
        serving_size=100.0,
        serving_unit="ml",
        serving_amount=250.0,
        energy_kcal=42.0,
        fats=2.5,
        carbohydrates=4.8,
        sugars=4.8,
        fibers=0.0,
        proteins=3.4
    )
    test_db.add(product3)

    test_db.commit()
    test_db.refresh(product1)
    test_db.refresh(product2)
    test_db.refresh(product3)

    return [product1, product2, product3]

@pytest.fixture
def sample_recipe_data(sample_products):
    """Sample recipe data for testing"""
    return {
        "name": "Pannenkoeken",
        "servings": 4, 
        "preparation_time": 30,
        "instructions": "1. Mix ingredients\n2. Cook in pan\n3. Serve hot",
        "image_url": "/api/recipes/1/image/test.jpg",
        "ingredients": [
            {
                "product_id": sample_products[0].id, # Bloem
                "amount": 250,
                "unit": "gram"
            },
            {
                "product_id": sample_products[1].id, # Eieren
                "amount": 3.0,
                "unit": "stuk"
            },
            {
                "product_id": sample_products[2].id, # Melk
                "amount": 500.0,
                "unit": "ml"
            }
        ]
    }

@pytest.fixture
def minimal_recipe_data(sample_products):
    """Minimal recipe data without optional fields"""
    return {
        "name": "Simple Recipe",
        "servings": 2,
        "preparation_time": 15,
        "instructions": "Mix and cook",
        "ingredients": [
            {
                "product_id": sample_products[0].id,
                "amount":100.0,
                "unit": "gram"
            }
        ]
    }

@pytest.fixture
def recipe_ingredient_data(sample_products):
    """Sample recipe ingredient data"""
    return {
        "product_id": sample_products[0].id,
        "amount": 200.0,
        "unit": "gram"
    }

@pytest.fixture
def menu_day_data():
    """Sample menu day data"""
    return {
        "date": date.today(),
        "recipe_id": 1,
        "servings": 4,
        "add_to_shopping_list": True
    }

@pytest.fixture
def menu_day_data_no_servings():
    """Sample menu day data"""
    return {
        "date": date.today(),
        "recipe_id": 1,
        "add_to_shopping_list": True
    }

@pytest.fixture
def week_menu_data():
    """Sample week menu data"""
    return {
        "start_date": date.today(),
        "end_date": date.today() + timedelta(days=1),
        "days": [
            {
                "date": date.today(),
                "recipe_id": 1,
                "servings": 4,
                "add_to_shopping_list": True
            },
            {
                "date": date.today() + timedelta(days=1),
                "recipe_id": 2,
                "servings": 2,
                "add_to_shopping_list": False
            }
        ]
    }