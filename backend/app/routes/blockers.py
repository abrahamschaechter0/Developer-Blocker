from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Blocker, BlockerCreate, BlockerRead, DescriptionUpdate, StatusUpdate

router = APIRouter(prefix="/blockers", tags=["blockers"])


def find_blocker(blocker_id: int, session: Session) -> Blocker:
    blocker = session.get(Blocker, blocker_id)
    if blocker is None:
        raise HTTPException(status_code=404, detail="Blocker not found")
    return blocker


@router.post("", response_model=BlockerRead, status_code=status.HTTP_201_CREATED)
def create_blocker(data: BlockerCreate, session: Session = Depends(get_session)):
    blocker = Blocker.model_validate(data)
    session.add(blocker)
    session.commit()
    session.refresh(blocker)
    return blocker


@router.get("", response_model=list[BlockerRead])
def list_blockers(session: Session = Depends(get_session)):
    return session.exec(select(Blocker).order_by(Blocker.id)).all()


@router.get("/{blocker_id}", response_model=BlockerRead)
def get_blocker(blocker_id: int, session: Session = Depends(get_session)):
    return find_blocker(blocker_id, session)


@router.put("/{blocker_id}/description", response_model=BlockerRead)
def update_description(blocker_id: int, data: DescriptionUpdate, session: Session = Depends(get_session)):
    blocker = find_blocker(blocker_id, session)
    blocker.description = data.description
    session.add(blocker)
    session.commit()
    session.refresh(blocker)
    return blocker


@router.patch("/{blocker_id}", response_model=BlockerRead)
def update_status(blocker_id: int, data: StatusUpdate, session: Session = Depends(get_session)):
    blocker = find_blocker(blocker_id, session)
    blocker.status = data.status
    session.add(blocker)
    session.commit()
    session.refresh(blocker)
    return blocker
