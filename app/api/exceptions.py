from fastapi import FastAPI
from fastapi import Request 
from fastapi import status

from fastapi.responses  import JSONResponse

from app.services.exceptions import UserEmailAlredyExistsException
from app.services.exceptions import UserNotFoundException
from app.services.exceptions import IncorrectPasswordException

from jwt import PyJWTError

def assign_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(PyJWTError)
    def invalid_token_handler(
        request: Request, 
        exc:     PyJWTError
    ) -> JSONResponse:
        return JSONResponse(
            status_code = status.HTTP_401_UNAUTHORIZED,
            content     = {"detail": "Invalid or expired token" },
            headers     = {"WWW-Authenticate": "Bearer"}
        )

    @app.exception_handler(IncorrectPasswordException)
    def user_not_found_handler(
        request: Request, 
        exc:     IncorrectPasswordException
    ) -> JSONResponse:
        return JSONResponse(
            status_code = status.HTTP_401_UNAUTHORIZED,
            content     = { "detail": "User unauthorized" },
        )

    @app.exception_handler(UserNotFoundException)
    def user_not_found_handler(
        request: Request, 
        exc:     UserNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content     = { "detail": "User not found" },
        )

    @app.exception_handler(UserEmailAlredyExistsException)
    def user_email_exists_handler(
        request: Request, 
        exc:     UserEmailAlredyExistsException
    ) -> JSONResponse:
        return JSONResponse(
            status_code = status.HTTP_409_CONFLICT,
            content     = { "detail": "User already registered" },
        )