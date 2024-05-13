from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Trade, TradeCreate, TradePublic, TradesPublic, TradeUpdate, Message

router = APIRouter()


@router.get("/", response_model=TradesPublic)
def read_trades(
        session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve trades.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Trade)
        count = session.exec(count_statement).one()
        statement = select(Trade).offset(skip).limit(limit)
        trades = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Trade)
            .where(Trade.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Trade)
            .where(Trade.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        trades = session.exec(statement).all()

    return TradesPublic(data=trades, count=count)


@router.get("/{id}", response_model=TradePublic)
def read_trade(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get trade by ID.
    """
    trade = session.get(Trade, id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if not current_user.is_superuser and (trade.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return trade


@router.post("/", response_model=TradePublic)
def create_trade(
        *, session: SessionDep, current_user: CurrentUser, trade_in: TradeCreate
) -> Any:
    """
    Create new trade.
    """
    trade = Trade.model_validate(trade_in, update={"owner_id": current_user.id})
    session.add(trade)
    session.commit()
    session.refresh(trade)
    return trade


@router.put("/{id}", response_model=TradePublic)
def update_trade(
        *, session: SessionDep, current_user: CurrentUser, id: int, trade_in: TradeUpdate
) -> Any:
    """
    Update an trade.
    """
    trade = session.get(Trade, id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if not current_user.is_superuser and (trade.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = trade_in.model_dump(exclude_unset=True)
    trade.sqlmodel_update(update_dict)
    session.add(trade)
    session.commit()
    session.refresh(trade)
    return trade


@router.delete("/{id}")
def delete_trade(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an trade.
    """
    trade = session.get(Trade, id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if not current_user.is_superuser and (trade.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(trade)
    session.commit()
    return Message(message="Trade deleted successfully")
