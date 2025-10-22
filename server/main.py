# =========================================== imports =============================================

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import asyncpg

# ======================================== database setup =========================================

# Database connection details
DATABASE_URL = "postgresql://p_user:p_password@localhost:5432/product_db"

# Establishing a connection to the database
async def connect(): return await asyncpg.connect(DATABASE_URL)

# Context manager to handle the database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await connect()
    try: yield
    finally: await app.state.db.close()

# =========================================== app setup ===========================================

# Creating a FastAPI instance
app = FastAPI(lifespan=lifespan)

# Setting up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================ routing  ===========================================

# root route, testing that the connection to the database works
@app.get("/")
async def root():
    try:
        await app.state.db.execute("SELECT 1")
        return {"message": "Hello World! Database connection is successful."}
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Bye World! Database connection failed.")
    
# get request to get the count of products in the database
@app.get("/products/count")
async def product_count():
    try:
        count: int = await app.state.db.fetchval("SELECT COUNT(*) FROM products")
        return {"count": count}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# get request to get all products in the database
@app.get("/products/all")
async def get_all_products(page: int = 1, limit: int = 10):
    try:
        offset = (page - 1) * limit
        selected_products = await app.state.db.fetch("SELECT * FROM products ORDER BY id LIMIT $1 OFFSET $2", limit, offset)
        return [dict(row) for row in selected_products]
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# get request to get a product by its id
@app.get("/products/{id}")
async def search_by_id(id: int):
    try:
        if id < 0:
            raise HTTPException(status_code=400, detail="Invalid ID")
        product = await app.state.db.fetchrow("SELECT * FROM products WHERE id = $1", id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product Not Found")
        return dict(product)
    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ======================================== run the app =========================================
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

# ==============================================================================================