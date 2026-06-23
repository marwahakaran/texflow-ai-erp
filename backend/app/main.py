from fastapi import FastAPI

from app.api import auth_v2, users_v2, roles_permissions, organization
from app.db import base, session
from app.core.config import settings
from app.core.middleware import AuditMiddleware

app = FastAPI(title="TexFlow AI ERP")

# include routers
app.include_router(auth_v2.router, prefix="/api/auth", tags=["auth"])
app.include_router(users_v2.router, prefix="/api/users", tags=["users"])
app.include_router(roles_permissions.router, prefix="/api/admin", tags=["admin"])
app.include_router(organization.router)

app.add_middleware(AuditMiddleware)

@app.on_event("startup")
async def on_startup():
    # Create DB tables in development if needed — use Alembic for migrations in prod
    engine = session.engine
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)

@app.get("/api/health")
async def health():
    return {"status": "ok", "db": settings.database_url}
