import uvicorn
from fastapi import FastAPI

from app.api import app_router
from app.api.exceptions import setup_handlers
from app.core import app_config
from app.core.lifespan import lifespan
from app.core.middlewares import setup_middlewares

app: FastAPI = FastAPI(
    debug=app_config.debug, title=app_config.project_name, lifespan=lifespan
)


setup_middlewares(app)
setup_handlers(app)
app.include_router(app_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_config.project_host,
        port=app_config.project_port,
        reload=True,  # для разработки
    )
