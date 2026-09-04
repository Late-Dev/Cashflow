import hmac
import hashlib
from urllib.parse import parse_qsl
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

    if not token or not init_data or not hash_str:
        return False, {}

    parsed = parse_qsl(init_data, keep_blank_values=True)
    received_hash = hash_str
    fields = []
    userData = {}

    for key, value in parsed:
        if key == "hash":
            received_hash = value
            continue
        if key == "user":
            userData = json.loads(value)
        fields.append((key, value))

    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(fields, key=lambda item: item[0])
    )

    secret_key = hmac.new(c_str.encode(), token.encode(), hashlib.sha256).digest()
    data_check = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)

    return hmac.compare_digest(data_check.hexdigest(), received_hash), userData


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
