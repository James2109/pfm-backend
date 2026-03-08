import bcrypt
import jwt
from jwt import PyJWKClient
from src.core.config import settings

_jwks_client = PyJWKClient(f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json")


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def decode_supabase_token(token: str) -> dict:
    signing_key = _jwks_client.get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["ES256"],
        audience="authenticated",
    )
