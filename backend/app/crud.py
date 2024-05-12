from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate

##########################################################################
## User
##########################################################################
def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


##########################################################################
## Item
##########################################################################

def create_item(*, session: Session, item_in: ItemCreate, owner_id: int) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

##########################################################################
## Company
##########################################################################

def create_company(*, session: Session, company_in: CompanyCreate, owner_id: int) -> Item:
    db_item = Company.model_validate(company_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def select_companies():
    with Session(engine) as session:
        statement = select(Company)
        results = session.exec(statement)
        return results


##########################################################################
## Bar
##########################################################################

def create_bar(*, session: Session, bar_in: BarCreate) -> Item:
    db_item = Bar.model_validate(bar_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def select_bars():
    with Session(engine) as session:
        statement = select(Bar)
        results = session.exec(statement)
        return results


##########################################################################
## Chart
##########################################################################

def create_chart(*, session: Session, chart_in: ChartCreate) -> Item:
    db_item = Chart.model_validate(bar_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def select_charts():
    with Session(engine) as session:
        statement = select(Chart)
        results = session.exec(statement)
        return results


##########################################################################
## FinancialStatement
##########################################################################

def create_financial_statement(*, session: Session, chart_in: FinancialStatementCreate) -> Item:
    db_item = FinancialStatement.model_validate(bar_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def select_financial_statements():
    with Session(engine) as session:
        statement = select(FinancialStatement)
        results = session.exec(statement)
        return results


##########################################################################
## Instrument
##########################################################################

def create_instrument(*, session: Session, instrument_in: InstrumentCreate) -> Item:
    db_item = Instrument.model_validate(instrument_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def select_instruments():
    with Session(engine) as session:
        statement = select(Instrument)
        results = session.exec(statement)
        return results


##########################################################################
## Order
###########################################################################

def create_order(*, session: Session, order_in: OrderCreate) -> Item:
    db_item = Order.model_validate(order_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def select_orders():
    with Session(engine) as session:
        statement = select(Order)
        results = session.exec(statement)
        return results


##########################################################################
## OrderLeg
###########################################################################

def create_order_leg(*, session: Session, order_leg_in: OrderLegCreate) -> Item:
    db_item = OrderLeg.model_validate(order_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item
def select_order_legs():
    with Session(engine) as session:
        statement = select(OrderLeg)
        results = session.exec(statement)
        return results


##########################################################################
## Portfolio
###########################################################################

def create_portfolio(*, session: Session, portfolio_in: PortfilioCreate) -> Item:
    db_item = Portfolio.model_validate(order_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def select_portfilios():
    with Session(engine) as session:
        statement = select(Portfolio)
        results = session.exec(statement)
        return results

##########################################################################
## Position
###########################################################################

def create_position(*, session: Session, position_in: PositionCreate) -> Item:
    db_item = Position.model_validate(position_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def select_positions():
    with Session(engine) as session:
        statement = select(Position)
        results = session.exec(statement)
        return results


##########################################################################
## Trade
###########################################################################

def create_trade(*, session: Session, trade_in: TradeCreate) -> Item:
    db_item = Trade.model_validate(trade_in)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def select_trades():
    with Session(engine) as session:
        statement = select(Trade)
        results = session.exec(statement)
        return results
