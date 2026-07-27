from fastapi import FastAPI
from fastapi import Request 
from fastapi import status

from fastapi.responses  import JSONResponse
from fastapi.exceptions import ResponseValidationError

from app.services.exceptions import UserEmailAlredyExistsException
from app.services.exceptions import UserNotFoundException

def assign_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(
        request: Request, 
        exc:     UserNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content     = {"detail": "User not found"},
        )

    @app.exception_handler(UserEmailAlredyExistsException)
    async def user_email_exists_handler(
        request: Request, 
        exc:     UserEmailAlredyExistsException
    ) -> JSONResponse:
        return JSONResponse(
            status_code = status.HTTP_409_CONFLICT,
            content     = {"detail": "User already registered"},
        )