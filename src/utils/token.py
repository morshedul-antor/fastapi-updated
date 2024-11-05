from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from schemas import TokenDataIn
from typing import Optional
from config import settings
from exceptions import *


class Token:

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=2)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def validate_token(token: str) -> TokenDataIn:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                options={"verify_sub": False}
            )
            user_id = payload.get("sub")

            if user_id is None:
                raise AppException.CredentialsException()

            token_data = TokenDataIn(user_id=user_id)
            return token_data

        except ExpiredSignatureError:
            raise AppException.BadRequest({"message": "Token has expired!"})
        except JWTError as err:
            print(err)
            raise AppException.CredentialsException()
