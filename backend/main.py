from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.product_routes import router as product_router
from routes.recipe_routes import router as recipe_router
from models.product import Base as ProductBase
from models.recipe import Base as RecipeBase
from config.database import engine

# Create tables
ProductBase.metadata.create_all(bind=engine)
RecipeBase.metadata.create_all(bind=engine)

app = FastAPI(title="Nutrition App API", version="1.0.0")

# CORS middleware for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(product_router)
app.include_router(recipe_router)

@app.get("/")
async def root():
    return {"message": "Nutrition App API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)