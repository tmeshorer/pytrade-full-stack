from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Instrument, InstrumentCreate, InstrumentPublic, InstrumentsPublic, InstrumentUpdate, Message

router = APIRouter()


@router.get("/", response_model=InstrumentsPublic)
def read_instruments(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve instruments.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Instrument)
        count = session.exec(count_statement).one()
        statement = select(Instrument).offset(skip).limit(limit)
        instruments = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Instrument)
            .where(Instrument.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Instrument)
            .where(Instrument.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        instruments = session.exec(statement).all()

    return InstrumentsPublic(data=instruments, count=count)


@router.get("/{id}", response_model=InstrumentPublic)
def read_instrument(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get instrument by ID.
    """
    instrument = session.get(Instrument, id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    if not current_user.is_superuser and (instrument.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return instrument


@router.post("/", response_model=InstrumentPublic)
def create_instrument(
    *, session: SessionDep, current_user: CurrentUser, instrument_in: InstrumentCreate
) -> Any:
    """
    Create new instrument.
    """
    instrument = Instrument.model_validate(instrument_in, update={"owner_id": current_user.id})
    session.add(instrument)
    session.commit()
    session.refresh(instrument)
    return instrument


@router.put("/{id}", response_model=InstrumentPublic)
def update_instrument(
    *, session: SessionDep, current_user: CurrentUser, id: int, instrument_in: InstrumentUpdate
) -> Any:
    """
    Update an instrument.
    """
    instrument = session.get(Instrument, id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    if not current_user.is_superuser and (instrument.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = instrument_in.model_dump(exclude_unset=True)
    instrument.sqlmodel_update(update_dict)
    session.add(instrument)
    session.commit()
    session.refresh(instrument)
    return instrument


@router.delete("/{id}")
def delete_instrument(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an instrument.
    """
    instrument = session.get(Instrument, id)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    if not current_user.is_superuser and (instrument.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(instrument)
    session.commit()
    return Message(message="Instrument deleted successfully")
