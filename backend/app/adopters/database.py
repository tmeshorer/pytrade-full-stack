from typing import Any

from sqlalchemy import func
from sqlmodel import select

from app.api.deps import SessionDep
from app.core.db_adopters import CompaniesRepo, AccountsRepo, InstrumentsRepo, OrdersRepo, PortfoliosRepo, TradesRepo
from app.models import Company, CompaniesPublic, Account, Instrument, Order, OrdersPublic, Portfolio, PortfoliosPublic, \
    Trade


#########################################################
# Companies
#########################################################

class DefaultCompaniesRepo(CompaniesRepo):

    def __init__(self, dep: SessionDep):
        self.__sessions = dep

    def get_company(self, id: int) -> Company:
        return self.__sessions.get(Company, id)

    def list_companies(self, skip: int = 0, limit: int = 100) -> Any:
        """
        List companies.
        """
        count_statement = select(func.count()).select_from(Company)
        count = self.__sessions.exec(count_statement).one()
        statement = select(Company).offset(skip).limit(limit)
        items = self.__sessions.exec(statement).all()
        return CompaniesPublic(data=items, count=count)

    def save(self, c: Company):
        self.__sessions.save(c)

    def create(self, c: Company):
        item = Company.model_validate(c)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def update(self, c: Company):
        item = self.__sessions.get(Company, id)
        if not item:
            raise ValueError("Company not found")
        update_dict = c.model_dump(exclude_unset=True)
        c.sqlmodel_update(update_dict)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def delete(self, id: int):
        item = self.__sessions.get(Company, id)
        if not item:
            raise ValueError("Company not found")
        self.__sessions.delete(item)
        self.__sessions.commit()


#########################################################
# Account
#########################################################

class DefaultAccountsRepo(AccountsRepo):

    def __init__(self, dep: SessionDep):
        self.__sessions = dep

    def get_account(self, id: int) -> Company:
        return self.__sessions.get(Account, id)

    def list_accounts(self, skip: int = 0, limit: int = 100) -> Any:
        """
        List companies.
        """
        count_statement = select(func.count()).select_from(Company)
        count = self.__sessions.exec(count_statement).one()
        statement = select(Company).offset(skip).limit(limit)
        items = self.__sessions.exec(statement).all()
        return CompaniesPublic(data=items, count=count)

    def save(self, c: Account):
        self.__sessions.save(c)

    def create(self, c: Account):
        item = Account.model_validate(c)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def update(self, c: Account):
        item = self.__sessions.get(Account, id)
        if not item:
            raise ValueError("Account not found")
        update_dict = c.model_dump(exclude_unset=True)
        c.sqlmodel_update(update_dict)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def delete(self, id: int):
        item = self.__sessions.get(Account, id)
        if not item:
            raise ValueError("Account not found")
        self.__sessions.delete(item)
        self.__sessions.commit()


#########################################################
# Instruments
#########################################################

class DefaultInstrumentsRepo(InstrumentsRepo):

    def __init__(self, dep: SessionDep):
        self.__sessions = dep

    def get_instrument(self, id: int) -> Company:
        return self.__sessions.get(Instrument, id)

    def list_instruments(self, skip: int = 0, limit: int = 100) -> Any:
        """
        List companies.
        """
        count_statement = select(func.count()).select_from(Instrument)
        count = self.__sessions.exec(count_statement).one()
        statement = select(Company).offset(skip).limit(limit)
        items = self.__sessions.exec(statement).all()
        return InstrumentsPublic(data=items, count=count)

    def save(self, c: Instrument):
        self.__sessions.save(c)

    def create(self, c: Instrument):
        item = Account.model_validate(c)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def update(self, c: Instrument):
        item = self.__sessions.get(Instrument, id)
        if not item:
            raise ValueError("Instrument not found")
        update_dict = c.model_dump(exclude_unset=True)
        c.sqlmodel_update(update_dict)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def delete(self, id: int):
        item = self.__sessions.get(Instrument, id)
        if not item:
            raise ValueError("Instrument not found")
        self.__sessions.delete(item)
        self.__sessions.commit()


#########################################################
# Orders
#########################################################

class DefaultOrdersRepo(OrdersRepo):

    def __init__(self, dep: SessionDep):
        self.__sessions = dep

    def get_order(self, id: int) -> Order:
        return self.__sessions.get(Order, id)

    def list_instruments(self, skip: int = 0, limit: int = 100) -> Any:
        """
        List companies.
        """
        count_statement = select(func.count()).select_from(Order)
        count = self.__sessions.exec(count_statement).one()
        statement = select(Company).offset(skip).limit(limit)
        items = self.__sessions.exec(statement).all()
        return OrdersPublic(data=items, count=count)

    def save(self, c: Order):
        self.__sessions.save(c)

    def create(self, c: Order):
        item = Order.model_validate(c)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def update(self, c: Order):
        item = self.__sessions.get(Order, id)
        if not item:
            raise ValueError("Order not found")
        update_dict = c.model_dump(exclude_unset=True)
        c.sqlmodel_update(update_dict)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def delete(self, id: int):
        item = self.__sessions.get(Order, id)
        if not item:
            raise ValueError("Order not found")
        self.__sessions.delete(item)
        self.__sessions.commit()


#########################################################
# Orders
#########################################################

class DefaultProtfoliosRepo(PortfoliosRepo):

    def __init__(self, dep: SessionDep):
        self.__sessions = dep

    def get_protfilio(self, id: int) -> Portfolio:
        return self.__sessions.get(Portfolio, id)

    def list_portfilios(self, skip: int = 0, limit: int = 100) -> Any:
        """
        List companies.
        """
        count_statement = select(func.count()).select_from(Portfolio)
        count = self.__sessions.exec(count_statement).one()
        statement = select(Portfolio).offset(skip).limit(limit)
        items = self.__sessions.exec(statement).all()
        return PortfoliosPublic(data=items, count=count)

    def save(self, c: Portfolio):
        self.__sessions.save(c)

    def create(self, c: Portfolio):
        item = Order.model_validate(c)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def update(self, c: Portfolio):
        item = self.__sessions.get(Portfolio, id)
        if not item:
            raise ValueError("Portfolio not found")
        update_dict = c.model_dump(exclude_unset=True)
        c.sqlmodel_update(update_dict)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def delete(self, id: int):
        item = self.__sessions.get(Portfolio, id)
        if not item:
            raise ValueError("Portfolio not found")
        self.__sessions.delete(item)
        self.__sessions.commit()


#########################################################
# Trades
#########################################################

class DefaultTradesRepo(TradesRepo):

    def __init__(self, dep: SessionDep):
        self.__sessions = dep

    def get_trade(self, id: int) -> Trade:
        return self.__sessions.get(Trade, id)

    def list_portfilios(self, skip: int = 0, limit: int = 100) -> Any:
        """
        List companies.
        """
        count_statement = select(func.count()).select_from(Trade)
        count = self.__sessions.exec(count_statement).one()
        statement = select(Portfolio).offset(skip).limit(limit)
        items = self.__sessions.exec(statement).all()
        return PortfoliosPublic(data=items, count=count)

    def save(self, c: Trade):
        self.__sessions.save(c)

    def create(self, c: Trade):
        item = Order.model_validate(c)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def update(self, c: Trade):
        item = self.__sessions.get(Trade, id)
        if not item:
            raise ValueError("Trade not found")
        update_dict = c.model_dump(exclude_unset=True)
        c.sqlmodel_update(update_dict)
        self.__sessions.add(item)
        self.__sessions.commit()
        self.__sessions.refresh(item)
        return item

    def delete(self, id: int):
        item = self.__sessions.get(Trade, id)
        if not item:
            raise ValueError("Trade not found")
        self.__sessions.delete(item)
        self.__sessions.commit()
