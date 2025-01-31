from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from app.core import app_config

http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=app_config.auth_jwt.token_url)
