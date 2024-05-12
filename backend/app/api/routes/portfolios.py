from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Portfolio, PortfolioCreate, PortfolioPublic, PortfoliosPublic, PortfolioUpdate, Message

router = APIRouter()


@router.get("/", response_model=PortfoliosPublic)
def read_portfolios(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve portfolios.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Portfolio)
        count = session.exec(count_statement).one()
        statement = select(Portfolio).offset(skip).limit(limit)
        portfolios = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Portfolio)
            .where(Portfolio.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Portfolio)
            .where(Portfolio.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        portfolios = session.exec(statement).all()

    return PortfoliosPublic(data=portfolios, count=count)


@router.get("/{id}", response_model=PortfolioPublic)
def read_portfolio(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get portfolio by ID.
    """
    portfolio = session.get(Portfolio, id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if not current_user.is_superuser and (portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return portfolio


@router.post("/", response_model=PortfolioPublic)
def create_portfolio(
    *, session: SessionDep, current_user: CurrentUser, portfolio_in: PortfolioCreate
) -> Any:
    """
    Create new portfolio.
    """
    portfolio = Portfolio.model_validate(portfolio_in, update={"owner_id": current_user.id})
    session.add(portfolio)
    session.commit()
    session.refresh(portfolio)
    return portfolio


@router.put("/{id}", response_model=PortfolioPublic)
def update_portfolio(
    *, session: SessionDep, current_user: CurrentUser, id: int, portfolio_in: PortfolioUpdate
) -> Any:
    """
    Update an portfolio.
    """
    portfolio = session.get(Portfolio, id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if not current_user.is_superuser and (portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = portfolio_in.model_dump(exclude_unset=True)
    portfolio.sqlmodel_update(update_dict)
    session.add(portfolio)
    session.commit()
    session.refresh(portfolio)
    return portfolio


@router.delete("/{id}")
def delete_portfolio(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an portfolio.
    """
    portfolio = session.get(Portfolio, id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if not current_user.is_superuser and (portfolio.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(portfolio)
    session.commit()
    return Message(message="Portfolio deleted successfully")
