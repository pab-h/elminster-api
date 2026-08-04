from fastapi import UploadFile

from uuid     import UUID
from sqlmodel import Session
from minio    import Minio
from pathlib  import Path
from uuid     import uuid4
from io       import BytesIO

from app.models   import Board
from app.services import users
from app.env      import settings

from app.schemas import BoardCreateSchema
from app.schemas import BoardReadSchema

from app.services.exceptions import BoardNotFoundException
from app.services.exceptions import NotAllowedToModifyException
from app.services.exceptions import WallpaperIsTooLargeException
from app.services.exceptions import WallpaperInvalidFormatException

def upload_wallpaper(
    id:        str,
    wallpaper: UploadFile,
    session:   Session,
    master_id: UUID,
    storage:   Minio
) -> BoardReadSchema:

    board = session.get(Board, UUID(id))

    if not board:
        raise BoardNotFoundException()

    users.find_user_by_id(
        id      = master_id,
        session = session
    )

    if str(board.master_id) != str(master_id):
        raise NotAllowedToModifyException()

    content = wallpaper.file.read()

    if len(content) > settings.max_wallpaper_size:
        raise WallpaperIsTooLargeException()

    if wallpaper.content_type not in (
        "image/png",
        "image/jpeg",
        "image/webp",
    ):
        raise WallpaperInvalidFormatException()

    if board.wallpaper:
        prefix = (
            f"{settings.garage_public_url}/"
            f"{settings.garage_default_bucket}/"
        )

        if board.wallpaper.startswith(prefix):
            board.wallpaper.removeprefix(prefix)


    extension   = Path(wallpaper.filename).suffix
    object_name = f"boards/{board.id}/wallpaper/{uuid4()}{extension}"

    storage.put_object(
        bucket_name  = settings.garage_default_bucket,
        object_name  = object_name,
        data         = BytesIO(content),
        length       = len(content),
        content_type = wallpaper.content_type,
    )

    board.wallpaper = (
        f"{settings.garage_public_url}/"
        f"{settings.garage_default_bucket}/"
        f"{object_name}"
    )

    session.add(board)
    session.commit()
    session.refresh(board)

    return board

def create_board(
    board_data: BoardCreateSchema,
    master_id:  UUID,
    session:    Session 
) -> BoardReadSchema:

    users.find_user_by_id(
        id      = master_id,
        session = session
    )

    board = Board(
      master_id   = master_id,
      title       = board_data.title,
      description = board_data.description,
    )

    session.add(board)
    session.commit()
    session.refresh(board)

    return board