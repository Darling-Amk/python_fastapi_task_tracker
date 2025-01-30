from fastapi.security import HTTPBearer, OAuth2PasswordBearer

# TODO  вынести в конфиг
http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
