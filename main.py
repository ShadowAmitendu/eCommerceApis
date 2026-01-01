import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Import your actual project modules here
# If you are just testing the UI, you can comment these out
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
    # Base.metadata.create_all(bind=engine)  # Uncomment for real DB

    if not os.path.exists("static"):
        os.makedirs("static")

    yield
    # Cleanup on shutdown


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
    allow_origins=["*"],
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
    client_ip = request.client.host
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

    return response


# Mount Static Files (CSS/JS/HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include your Routers
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(admin.router)


# --- HTML Page Endpoints ---

@app.get("/", include_in_schema=False)
def root():
    """Serves the Home Page"""
    return FileResponse("static/index.html")


@app.get("/health")
def health_check():
    """JSON Health Check"""
    return {"status": "healthy"}


@app.get("/status", include_in_schema=False)
def status_page():
    """Serves the Status Dashboard"""
    return FileResponse("static/status.html")


@app.get("/incidents", include_in_schema=False)
def incidents_page():
    """Serves the Incident Management Page"""
    return FileResponse("static/incidents.html")


@app.get("/docs", include_in_schema=False)
async def documentation_landing():
    """Serves the Documentation Selection Page"""
    return FileResponse("static/docs-landing.html")


# --- Documentation Logic ---

@app.get("/docs-swagger", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Serves the STATIC Swagger HTML file.
    This fixes the styling/layout issues by bypassing FastAPI's generator.
    """
    return FileResponse("static/swagger.html")


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
    return {"incidents": []}
