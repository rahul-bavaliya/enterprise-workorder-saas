"""
API v1 router.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    work_orders,
    assets,
    branch,
    make_product_model,
)

api_router = APIRouter()

# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    work_orders.router, prefix="/work-orders", tags=["work-orders"]
)
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(branch.router, prefix="/branches", tags=["branches"])
# api_router.include_router(line_of_business.router, prefix="/line-of-business", tags=["line-of-business"])
api_router.include_router(
    make_product_model.router,
    prefix="/make-product-models",
    tags=["make-product-models"],
)
# api_router.include_router(business.router, prefix="/businesses", tags=["businesses"])
# api_router.include_router(department.router, prefix="/departments", tags=["departments"])
