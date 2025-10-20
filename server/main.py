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
# your code here

# get request to get all products in the database
# your code here

# get request to get a product by its id
# your code here

# ======================================== run the app =========================================
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

# ==============================================================================================