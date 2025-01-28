from fastapi import APIRouter
from fastapi.params import Depends

from app.auth import utils
from app.auth.auth_dependencies import get_jwt_service, valid_auth_user
from app.auth.schemas.token_schema import TokenInfo
from app.auth.schemas.user_auth_schema import UserAuth
from app.auth.services.jwt_service import AuthJWTService

router = APIRouter()


# Получение всех пользователей
@router.post("/login")
async def auth_user_issue_jwt(
    user: UserAuth = Depends(valid_auth_user),
    auth_jwt_service: AuthJWTService = Depends(get_jwt_service),
) -> TokenInfo:
    token: str = auth_jwt_service.encode_jwt(utils.create_payload_from_user_read(user))
    return TokenInfo(access_token=token, token_type="Bearer")
