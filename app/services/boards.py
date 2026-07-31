from uuid     import UUID
from sqlmodel import Session

from app.models   import Board
from app.services import users

from app.schemas import BoardCreateSchema
from app.schemas import BoardReadSchema

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

    