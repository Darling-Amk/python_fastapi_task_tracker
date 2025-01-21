from fastapi import APIRouter

router = APIRouter()

# Получение всех пользователей
@router.get("/")
def test():
    """
    Получить список всех пользователей.
    """
    users = [
        {
            "username": "Amk",
            "email": "Amk",
            "id": 1,
        },
    ]