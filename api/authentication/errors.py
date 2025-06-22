from fastapi import status

INCORRECT_CREDENTIALS = {
    "status_code": status.HTTP_401_UNAUTHORIZED,
    "detail": "Incorrect username or password",
    "headers": {"WWW-Authenticate": "Bearer"},
}

ILLEGAL_EXPIRED_TOKEN = {
    "status_code": status.HTTP_401_UNAUTHORIZED,
    "detail": "Token is either illegal or expired",
    "headers": {"WWW-Authenticate": "Bearer"},
}
