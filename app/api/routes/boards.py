from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import UploadFile

from uuid     import UUID
from sqlmodel import Session
from minio    import Minio

from app.storage  import get_storage
from app.database import get_db_session
from app.services import boards

from app.schemas import BoardCreateSchema
from app.schemas import BoardReadSchema

from app.api.authentication import get_current_user_id

router = APIRouter(
    tags   = ["Boards"], 
    prefix = "/boards"
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_board(
    board_data: BoardCreateSchema,
    session:    Session            = Depends(get_db_session),
    master_id:  UUID               = Depends(get_current_user_id)
) -> BoardReadSchema:

    return boards.create_board(
        board_data = board_data,
        master_id  = master_id,
        session    = session
    )

@router.post("/{id}/wallpaper", status_code = status.HTTP_201_CREATED)
def upload_wallpaper(
    id:        str,
    wallpaper: UploadFile,      
    session:   Session = Depends(get_db_session),
    master_id: UUID    = Depends(get_current_user_id),
    storage:   Minio   = Depends(get_storage)
) -> BoardReadSchema:

    return boards.upload_wallpaper(
        id        = id,
        wallpaper = wallpaper,      
        session   = session,
        master_id = master_id,
        storage   = storage
    )