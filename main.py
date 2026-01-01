import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Import database for initialization
from database import Base, engine
# Import routers
from routers import auth, product, admin

# --- Global Metrics Store (In-Memory) ---
# This holds the real-time data for the Status Page
METRICS = {
    "total_requests": 0,
    "total_errors": 0,
    "total_latency_seconds": 0.0,
    "active_ips": {}  # Maps IP -> timestamp
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events:
    1. Initialize Database
    2. Ensure static folder exists
    """
    # Create database tables if they don't exist
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    # Ensure static folder exists
    if not os.path.exists("static"):
        os.makedirs("static")
        print("Static folder created")

    yield

    # Cleanup on shutdown
    print("Shutting down...")


app = FastAPI(
    title="E-Commerce REST API",
    description="A secure e-commerce API with authentication and role-based access",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,  # Disable default Swagger
    redoc_url=None  # Disable default ReDoc
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Middleware: Real-Time Traffic Monitor ---
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    """
    Middleware to calculate response times and track active users
    for the Status Page.
    """
    start_time = time.time()

    # 1. Record Active User (IP based)
    client_ip = request.client.host if request.client else "unknown"
    METRICS["active_ips"][client_ip] = start_time

    # Process the request
    response = await call_next(request)

    # 2. Calculate Processing Time
    process_time = time.time() - start_time

    # 3. Update Global Counters
    METRICS["total_requests"] += 1
    METRICS["total_latency_seconds"] += process_time

    # 4. Track Errors (HTTP 500s)
    if response.status_code >= 500:
        METRICS["total_errors"] += 1

    # Add response time header for debugging
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Mount Static Files (CSS/JS/HTML)
# Make sure the static folder exists with all HTML files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    print("Warning: static folder not found. Some routes may not work.")

# Include your Routers
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(admin.router)


# --- HTML Page Endpoints ---

@app.get("/", include_in_schema=False)
def root():
    """Serves the Home Page"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "E-Commerce API is running", "docs": "/docs"}


@app.get("/health")
def health_check():
    """JSON Health Check"""
    return {
        "status": "healthy",
        "service": "E-Commerce API",
        "version": "1.0.0"
    }


@app.get("/status", include_in_schema=False)
def status_page():
    """Serves the Status Dashboard"""
    if os.path.exists("static/status.html"):
        return FileResponse("static/status.html")
    return {"message": "Status page not found", "metrics_api": "/api/metrics"}


@app.get("/incidents", include_in_schema=False)
def incidents_page():
    """Serves the Incident Management Page"""
    if os.path.exists("static/incidents.html"):
        return FileResponse("static/incidents.html")
    return {"message": "Incidents page not found"}


@app.get("/docs", include_in_schema=False)
async def documentation_landing():
    """Serves the Documentation Selection Page"""
    if os.path.exists("static/docs-landing.html"):
        return FileResponse("static/docs-landing.html")
    return {"swagger": "/docs-swagger", "redoc": "/docs-redoc"}


# --- Documentation Logic ---

@app.get("/docs-swagger", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Serves the STATIC Swagger HTML file.
    This fixes the styling/layout issues by bypassing FastAPI's generator.
    """
    if os.path.exists("static/swagger.html"):
        return FileResponse("static/swagger.html")
    return {"message": "Swagger UI not found", "openapi": "/openapi.json"}


@app.get("/docs-redoc", include_in_schema=False)
async def redoc_html():
    """Serves ReDoc using FastAPI's helper (styled in landing page)"""
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    )


# --- API Endpoints for Frontend Data ---

@app.get("/api/metrics")
def get_live_metrics():
    """
    Returns real metrics calculated by the middleware.
    Consumed by static/status.html
    """
    total = METRICS["total_requests"]
    errors = METRICS["total_errors"]
    latency = METRICS["total_latency_seconds"]

    # Filter active users (active in last 5 minutes)
    now = time.time()
    METRICS["active_ips"] = {
        ip: ts for ip, ts in METRICS["active_ips"].items()
        if now - ts < 300
    }

    avg_latency_ms = (latency / total * 1000) if total > 0 else 0
    error_rate = (errors / total * 100) if total > 0 else 0

    return {
        "request_count": total,
        "avg_response_time": round(avg_latency_ms, 2),
        "error_rate": round(error_rate, 2),
        "active_users": len(METRICS["active_ips"])
    }


@app.get("/api/incidents")
def get_incidents_api():
    """
    Placeholder for incident data.
    In this demo, the frontend uses LocalStorage, but this endpoint
    could be connected to a database later.
    """
    return {"incidents": [], "message": "No incidents reported"}


# --- Root API Info (for API clients) ---
@app.get("/api")
def api_info():
    """API Information endpoint"""
    return {
        "name": "E-Commerce REST API",
        "version": "1.0.0",
        "documentation": {
            "swagger": "/docs-swagger",
            "redoc": "/docs-redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "health": "/health",
            "metrics": "/api/metrics",
            "auth": "/auth/*",
            "products": "/products/*",
            "admin": "/admin/*"
        }
    }


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
