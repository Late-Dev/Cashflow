import hmac
import hashlib
from urllib.parse import unquote
from datetime import datetime, timedelta
import json
import jwt


def validate_initData(hash_str, init_data, token, c_str="WebAppData") -> bool:
    """
    Validates the data received from the Telegram web app, using the
    method documented here:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    hash_str - the hash string passed by the webapp
    init_data - the query string passed by the webapp
    token - Telegram bot's token
    c_str - constant string (default = "WebAppData")
    """

    init_data = sorted([ chunk.split("=")
          for chunk in unquote(init_data).split("&")
            if chunk[:len("hash=")]!="hash="],
        key=lambda x: x[0])
    user = [item for item in init_data if item[0] == 'user']

    userData = json.loads(user[0][1])

    init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])

    secret_key = hmac.new(c_str.encode(), token.encode(),
        hashlib.sha256 ).digest()
    data_check = hmac.new( secret_key, init_data.encode(),
        hashlib.sha256)

    return data_check.hexdigest() == hash_str, userData


def create_access_token(
        SECRET_KEY: str,
        ALGORITHM: str,
        ACCESS_TOKEN_EXPIRE_MINUTES: int,
        data: dict,
        expires_delta: timedelta | None = None
    ):
    to_encode = data.copy()
    to_encode.update({'iat': datetime.utcnow()})
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

