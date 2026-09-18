# app/main.py
import logging

from fastapi import FastAPI

from app.core.logging import setup_logging

from app.modules.tenant.router import router as tenant_router
from app.modules.work_order.router import router as work_order_router
from app.modules.branch.router import router as branch_router

from app.core.exceptions import register_exception_handlers


# Initialize logging configuration
setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Enterprise Work-Order SaaS",
    description="Enterprise multi-tenant work-order management system with explicit routing.",
    version="0.1.0",
)

register_exception_handlers(app)

# Explicitly register module routers
app.include_router(tenant_router)
app.include_router(work_order_router)
app.include_router(branch_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Enterprise Work-Order SaaS backend...")


@app.get("/")
def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "healthy"}
