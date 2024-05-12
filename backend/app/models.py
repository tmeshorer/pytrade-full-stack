import datetime
import enum

from sqlmodel import Field, Relationship, SQLModel

# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


##########################################################################
## Account
##########################################################################

class AccountBase(SQLModel):
    broker: str
    buying_power: float = 0
    cash: float = 0
    currency: str = "USD"
    daytrade_count: int = 0
    equity:float = 0

class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    portfolios: list["Porfolio"] = Relationship(back_populates="account")
    orders: list["Order"] = Relationship(back_populates="account")

# Properties to receive on account creation
class AccountCreate(AccountBase):
    pass

# Properties to receive on account update
class AccountUpdate(AccountBase):
    pass

# Properties to return via API, id is always required
class AccountPublic(AccountBase):
    id: int


class AccountsPublic(SQLModel):
    data: list[AccountPublic]
    count: int


##########################################################################
## Company
##########################################################################

class CompanyBase(SQLModel):
    name: str
    sector: str | None = None
    subsector: str | None = None
    market_cap: float = 0

class Company(CompanyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    instruments: list["Instrument"] = Relationship(back_populates="instrument")

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class CompanyPublic(CompanyBase):
    id: int

class CompaniesPublic(SQLModel):
    data: list[CompanyPublic]
    count: int


##########################################################################
## FinancialStatement
##########################################################################

class FSType(enum.Enum):
    BALANCE_SHEET = "balancesheet"
    INCOME = "income"
    CASHFLOW = "cashflow"

class FinanicalStatementBase(SQLModel):
    st_type: FSType
    qtr: int
    year: int

class FinanicalStatement(FinanicalStatementBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    company_id: int | None = Field(default=None, foreign_key="company.id", nullable=False)
    company: Company | None = Relationship(back_populates="companies")

    items: list["FinancialStatementLineItemBase"] = Relationship(back_populates="financial_statement")

class FinancialStatementCreate(FinanicalStatementBase):
    pass

class FinancialStatementPublic(CompanyBase):
    id: int

class FinancialStatementsPublic(SQLModel):
    data: list[FinancialStatementPublic]
    count: int

##########################################################################
## FinancialStatementLineItem
##########################################################################

class FinancialStatementLineItemBase(SQLModel):
    name: str
    amount: float

class FinancialStatementLineItem(FinancialStatementLineItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    financial_statement_id: int | None = Field(default=None, foreign_key="financialstatement.id", nullable=False)
    financial_statement: FinanicalStatement | None = Relationship(back_populates="financial_statements")


class FinancialStatementLineItemCreate(FinanicalStatementBase):
    pass

##########################################################################
## Instrument
##########################################################################

class AssetType(enum.Enum):
    STOCK = "stock"
    OPTION = "option"
    FOREX = "forex"
    FUTURE = "future"
    ETF = "etf"


class InstrumentBase(SQLModel):
    symbol: str
    asset_type: AssetType
    currency: str = "USD"
    exchange: str | None
    root: str | None
    underlying: str | None
    avg_daily_volume: float | None = None
    one_year_return: float | None = None
    one_month_return: float | None = None
    one_week_return: float | None = None
    one_day_return: float | None = None
    metric_52_high: float | None = None
    metric_52_low: float | None = None

class Instrument(InstrumentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    company_id: int | None = Field(default=None, foreign_key="company.id", nullable=False)
    company: Company | None = Relationship(back_populates="companies")

    charts: list["Chart"] = Relationship(back_populates="instrument")


class InstrumentCreate(InstrumentBase):
    pass

class InstrumentPublic(InstrumentBase):
    id: int

class InstrumentsPublic(SQLModel):
    data: list[InstrumentPublic]
    count: int



##########################################################################
## Chart
##########################################################################
class ChartInterval(enum.Enum):
    Min_5   = "5min"
    Min_15  = "15min"
    Min_30  = "30min"
    Hourly  = "hourly"
    Daily   = "daily"
    Monthly = "monthly"

class ChartBase(SQLModel):
    interval: ChartInterval
    timestamp: datetime

class Chart(ChartBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    instrument_id: int | None = Field(default=None, foreign_key="instrument.id", nullable=False)
    instrument: Instrument | None = Relationship(back_populates="instruments")

    bars: list["Bar"] = Relationship(back_populates="chart")

class ChartCreate(ChartBase):
    pass

class ChartUpdate(ChartBase):
    pass

class ChartPublic(ChartBase):
    id: int

class ChartsPublic(SQLModel):
    data: list[ChartPublic]
    count: int



##########################################################################
## Bar
##########################################################################

class BarBase(SQLModel):
    timestamp: datetime
    loc: int
    high: float
    low: float
    open: float
    close: float
    volume: float
    downTicks: float | None
    downVolume: float | None
    totalTicks: float | None
    upTicks: float | None
    upVolume: float | None
    symbol : str

class Bar(BarBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    instrument_id: int | None = Field(default=None, foreign_key="instrument.id", nullable=False)
    instrument: Instrument | None = Relationship(back_populates="instruments")

    chart_id: int | None = Field(default=None, foreign_key="chart.id", nullable=False)
    chart: Chart | None = Relationship(back_populates="charts")

class BarCreate(BarBase):
    pass


##########################################################################
## Portfolio
##########################################################################

class PortfolioBase(SQLModel):
    cash: float
    equity: float
    profit: float

class Porfolio(PortfolioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    account_id: int | None = Field(default=None, foreign_key="account.id")
    account: Account | None = Relationship(back_populates="accounts")

    positions: list["Position"] = Relationship(back_populates="portfolio")
    orders: list["Order"] = Relationship(back_populates="order")



class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(PortfolioBase):
    pass

class PortfolioPublic(PortfolioBase):
    id: int

class PortfoliosPublic(SQLModel):
    data: list[PortfolioPublic]
    count: int



##########################################################################
## Order
##########################################################################

class OrderType(enum.Enum):
    LIMIT = "limit"
    MARKET = "market"
    STOP = "stop"

class TimeInForce(enum.Enum):
    DAY = "day"
    GTC = "gtc"

class QtyUnits(enum.Enum):
   SHARES = "shares"
   USD = "usd"


class OrderBase(SQLModel):
    currency: str
    symbol: str
    open_date_time: str
    order_type: OrderType
    qty: float
    price: float
    unit: QtyUnits
    time_in_force: TimeInForce
    status: str | None

class Order(OrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    portfolio_id: int | None = Field(default=None, foreign_key="portfolio.id")
    porfolio: Porfolio | None = Relationship(back_populates="porfolios")

    instrument_id: int | None = Field(default=None, foreign_key="instrument.id")
    instrument: Instrument | None = Relationship(back_populates="instruments")

    legs: list["OrderLeg"] = Relationship(back_populates="order")

class OrderCreate(OrderBase):
    pass
class OrderUpdate(OrderBase):
    pass

class OrderPublic(OrderBase):
    id: int

class OrdersPublic(SQLModel):
    data: list[OrderPublic]
    count: int



##########################################################################
## Order Leg
##########################################################################


class OrderLegBase(SQLModel):
    order_type: OrderType
    qty: float
    price: float
    status: str

class OrderLeg(OrderLegBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parent_id: int | None = Field(default=None, foreign_key="order.id")
    parent: Order | None = Relationship(back_populates="orders")

class OrderLegCreate(OrderBase):
    pass

class OrderLegUpdate(OrderBase):
    pass


##########################################################################
## Position
##########################################################################

class PositionDirection(enum.Enum):
   LONG = "long"
   SHORT = "short"
class PositionBase(SQLModel):
    long_short : PositionDirection
    qty: float
    cost: float | None
    market_value: float | None

class Position(PositionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    portfolio_id : int | None = Field(default=None, foreign_key="portfolio.id")
    portfolio: Porfolio | None = Relationship(back_populates="portfolios")

    instrument_id: int | None = Field(default=None, foreign_key="instrument.id")
    instrument: Instrument | None = Relationship(back_populates="instruments")

    orders: list["Order"] = Relationship(back_populates="position")

class PositionCreate(OrderBase):
    pass

class PositionUpdate(OrderBase):
    pass

class PositionPublic(OrderBase):
    id: int

class PositionsPublic(SQLModel):
    data: list[PositionPublic]
    count: int


##########################################################################
## Trade
##########################################################################


class TradeBase(SQLModel):
    qty: float
    entry_price: float
    exit_price: float

class Trade(TradeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    portfolio_id: int | None = Field(default=None, foreign_key="portfolio.id")
    portfolio: Porfolio | None = Relationship(back_populates="portfolios")

    instrument_id: int | None = Field(default=None, foreign_key="instrument.id")
    instrument: Instrument | None = Relationship(back_populates="instruments")

    entry_signal_bar_id: int | None = Field(default=None, foreign_key="bar.id")
    entry_signal_bar: Bar | None = Relationship(back_populates="bars")

    entry_action_bar_id: int | None = Field(default=None, foreign_key="bar.id")
    entry_action_bar: Bar | None = Relationship(back_populates="bars")

    entry_order_id: int | None = Field(default=None, foreign_key="order.id")
    entry_order_bar: Bar | None = Relationship(back_populates="orders")

    exist_signal_bar_id: int | None = Field(default=None, foreign_key="bar.id")
    exit_signal_bar: Bar | None = Relationship(back_populates="bars")

    exit_action_bar_id: int | None = Field(default=None, foreign_key="bar.id")
    exit_action_bar: Bar | None = Relationship(back_populates="bars")

    exit_order_id: int | None = Field(default=None, foreign_key="order.id")
    exit_order_bar: Bar | None = Relationship(back_populates="orders")

    position_id: int | None = Field(default=None, foreign_key="position.id")
    position: Position | None = Relationship(back_populates="positions")





class TradeCreate(OrderBase):
    pass

class TradeUpdate(OrderBase):
    pass

class TradePublic(TradeBase):
    id: int

class TradesPublic(SQLModel):
    data: list[TradePublic]
    count: int
