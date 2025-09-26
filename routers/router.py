from fastapi import APIRouter
from app.routes import select_routes, voice_routes, language_routes, service_routes
# test3/routers/router.py

from fastapi import APIRouter
from app.routes import (
    user,
    clover_auth,
    clover_data,
    select_routes,
    voice_routes,
    question_master,
    clover_cart,
    userCart,
    cart,
    language_routes,
    merchant_categories,
    merchant_routes,
    orderProcess,
    service_routes,
    # New additions from test2
    items,
    merchants,
    recommendations,
)

# This is our single main router
router = APIRouter()

# Include all the individual routers with their prefixes
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(clover_auth.router, prefix="/clover", tags=["clover"])
router.include_router(clover_data.router, prefix="/clover-data", tags=["clover-data"])
router.include_router(select_routes.router, prefix="/selectable-data", tags=["selectable-data"])
router.include_router(voice_routes.router, prefix="/voice", tags=["voice"])
router.include_router(question_master.router, prefix="/question-master", tags=["question-master"])
router.include_router(clover_cart.router, prefix="/clover-cart", tags=["clover-cart"])
router.include_router(userCart.router, prefix="/user-cart", tags=["user-cart"])
router.include_router(cart.router, prefix="/cart", tags=["cart"])
router.include_router(language_routes.router, prefix="/languages", tags=["languages"])
router.include_router(merchant_categories.router, prefix="/merchant-categories", tags=["merchant-categories"])
router.include_router(merchant_routes.router, prefix="/merchants-new", tags=["merchants-new"]) # Renamed tag to avoid conflict
router.include_router(orderProcess.router, prefix="/order-process", tags=["order-process"])
router.include_router(service_routes.router, prefix="/services", tags=["services"])

# --- Add the new routers from test2 ---
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(merchants.router, prefix="/merchants", tags=["merchants"])
router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])


api_router = APIRouter()

# Include route modules
api_router.include_router(
    select_routes.router,
    prefix="/select",
    tags=["Select Mode"]
)

api_router.include_router(
    voice_routes.router,
    prefix="/voice",
    tags=["Voice Mode"]
)

api_router.include_router(
    language_routes.router,
    prefix="/language",
    tags=["Language Selection"]
)

api_router.include_router(
    service_routes.router,
    prefix="/service",
    tags=["Service Selection"]
)
