from typing import TypedDict

from pydantic import EmailStr


class UserPayload(TypedDict):
    sub: str  # id
    id: int  # id
    name: str
    email: EmailStr | str
