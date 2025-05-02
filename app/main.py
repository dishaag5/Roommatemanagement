from fastapi import FastAPI
from app.database import Base, engine
from app.auth import auth_router
from app.households import household_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router)
app.include_router(household_router)

@app.get("/")
def read_root():
    return {"message": "Roommate Management API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)