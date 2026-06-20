from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
from app.db.session import SessionLocal
from app.db.models.audit import AuditLog
import json
import asyncio

class AuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        try:
            # best-effort: write small audit record async
            async def write_audit():
                async with SessionLocal() as db:
                    payload = {
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                    }
                    user_id = None
                    if hasattr(request.state, "user") and request.state.user:
                        try:
                            user_id = str(request.state.user.id)
                        except Exception:
                            user_id = None
                    audit = AuditLog(user_id=user_id, action=request.url.path, payload=payload)
                    db.add(audit)
                    await db.commit()
            asyncio.create_task(write_audit())
        except Exception:
            pass
        return response
