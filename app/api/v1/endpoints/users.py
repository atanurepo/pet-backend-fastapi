from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.crud.user import user_crud
from app.crud.user import create_user

from app.crud.user import scd2_update_user

from uuid import UUID
from fastapi import HTTPException


from app.crud.user import get_current_user_by_user_id
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user_api(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    ):
    return create_user(db, user_in)

@router.get(
    "/",
    response_model=list[UserRead],
)
def get_users(
    db: Session = Depends(get_db),
):
    return user_crud.get_all(db)

@router.get(
    "/{user_id}",
    response_model=UserRead,
)
def get_user_by_user_id(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    user = get_current_user_by_user_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user

@router.get("/{user_id}/history", response_model=list[UserRead])
def get_user_history(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .order_by(User.version_no)
        .all()
    )


@router.put(
    "/{user_id}",
    response_model=UserRead,
)
def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
):
    updated_user = scd2_update_user(db, user_id, user_in)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user