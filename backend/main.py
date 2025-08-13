from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.product_routes import router as product_router
from routes.recipe_routes import router as recipe_router
from routes.weekmenu_routes import router as weekmenu_router
from routes.shopping_list_routes import router as shopping_list_router
from routes.daily_food_routes import router as daily_food_router
from models.product import Base as ProductBase
from models.recipe import Base as RecipeBase
from models.weekmenu import Base as WeekMenuBase
from models.daily_food_log import Base as DailyFoodBase
from config.database import engine
from fastapi.staticfiles import StaticFiles

# Create tables
ProductBase.metadata.create_all(bind=engine)
RecipeBase.metadata.create_all(bind=engine)
WeekMenuBase.metadata.create_all(bind=engine)
DailyFoodBase.metadata.create_all(bind=engine)

app = FastAPI(title="Nutrition App API", version="1.0.0")

# CORS middleware for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(product_router)
app.include_router(recipe_router)
app.include_router(weekmenu_router)
app.include_router(shopping_list_router)
app.include_router(daily_food_router)

@app.get("/")
async def root():
    return {"message": "Nutrition App API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)