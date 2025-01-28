from typing import Dict, Any

from app.auth.schemas.user_auth_schema import UserAuth


def create_payload_from_user_read(user_read_schema: UserAuth) -> Dict[str, Any]:
    return {
        "sub": user_read_schema.id,
        "name": user_read_schema.name,
        "email": user_read_schema.email,
    }
