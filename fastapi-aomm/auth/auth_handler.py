# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict

import jwt
from decouple import config
import base64

from functools import lru_cache
import app_config

@lru_cache
def get_settings():
    return app_config.Settings()

JWT_SECRET = config("secret", default=get_settings().secret)
JWT_ALGORITHM = config("algorithm", default=get_settings().algorithm)

def encode_session(user_id: str) -> str:
    user_id_bytes = user_id.encode("ascii")
    session_bytes = base64.b64encode(user_id_bytes)
    return session_bytes.decode("ascii")

def decode_session(session_id: str) -> str:
    session_id_bytes = session_id.encode("ascii")
    user_id_bytes = base64.b64decode(session_id_bytes)
    return user_id_bytes.decode("ascii")    

def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

# function used for signing the JWT string
def signoutJWT(session_id: str) -> Dict[str, str]:
    user_id = decode_session(session_id)
    payload = {
        "user_id": user_id,
        "expires": time.time() - 500
    }
    print(payload["user_id"], payload["expires"])
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}