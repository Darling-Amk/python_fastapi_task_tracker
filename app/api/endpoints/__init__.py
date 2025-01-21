from fastapi import APIRouter

from app.api.endpoints import auth, projects, tasks, users, project_managment

app_router = APIRouter()

# Подключение маршрутов
# app_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
app_router.include_router(
    project_managment.router, prefix="/project_management", tags=["Project Management"]
)
app_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
app_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app_router.include_router(users.router, prefix="/users", tags=["Users"])
