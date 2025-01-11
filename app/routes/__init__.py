# backend/app/routes/__init__.py

from .cve import router as cve_router

__all__ = ["cve_router"]