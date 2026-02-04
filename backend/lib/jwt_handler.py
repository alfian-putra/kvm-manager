import time
from typing import Dict

import jwt
from decouple import config
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .common_utility import config as cfg
from .common_utility import log


JWT_SECRET = cfg["jwt"]["secret"]
JWT_ALGORITHM = cfg["jwt"]["algorithm"]
JWT_EXPIRATION_MINUTE = cfg["jwt"]["expiration"]
SECURITY = HTTPBearer()


def token_response(token: str):
    log.debug('{ "token : "'+ token +'}')
    return {
        "token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    import json

    exp = time.time() + (60 * JWT_EXPIRATION_MINUTE)
    exp_format = time.gmtime(exp)
    str_exp_format = time.strftime("%D %T", exp_format)
    
    payload = {
        "user_id": user_id,
        "expires": exp
    }

    log.debug(f'Generating jwt for {id} : '+repr(payload))
    log.debug(f'Expired on : {str_exp_format}')

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    log.debug(f'JWT token : {token}')

    return token_response(token)

def decodeJWT(token: str) -> dict:
    log.info(f"Decoding token : {token}")

    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None


async def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(SECURITY)):
    token = credentials.credentials
    payload = decodeJWT(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return payload