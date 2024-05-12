from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Company, CompanyCreate, CompanyPublic, CompaniesPublic, CompanyUpdate, Message

router = APIRouter()


@router.get("/", response_model=CompaniesPublic)
def read_companies(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve companys.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Company)
        count = session.exec(count_statement).one()
        statement = select(Company).offset(skip).limit(limit)
        companys = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Company)
            .where(Company.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Company)
            .where(Company.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        companys = session.exec(statement).all()

    return CompaniesPublic(data=companys, count=count)


@router.get("/{id}", response_model=CompanyPublic)
def read_company(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get company by ID.
    """
    company = session.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if not current_user.is_superuser and (company.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return company


@router.post("/", response_model=CompanyPublic)
def create_company(
    *, session: SessionDep, current_user: CurrentUser, company_in: CompanyCreate
) -> Any:
    """
    Create new company.
    """
    company = Company.model_validate(company_in, update={"owner_id": current_user.id})
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


@router.put("/{id}", response_model=CompanyPublic)
def update_company(
    *, session: SessionDep, current_user: CurrentUser, id: int, company_in: CompanyUpdate
) -> Any:
    """
    Update an company.
    """
    company = session.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if not current_user.is_superuser and (company.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = company_in.model_dump(exclude_unset=True)
    company.sqlmodel_update(update_dict)
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


@router.delete("/{id}")
def delete_company(session: SessionDep, current_user: CurrentUser, id: int) -> Message:
    """
    Delete an company.
    """
    company = session.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if not current_user.is_superuser and (company.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(company)
    session.commit()
    return Message(message="Company deleted successfully")
