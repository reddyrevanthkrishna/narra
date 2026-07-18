from fastapi import FastAPI

app = FastAPI(
    title="Narra API",
    version="1.0.0",
    description="Backend API for the Narra premium resale marketplace.",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Narra API 🚀"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }