from abc import ABC, abstractmethod
from typing import Optional, List

from app.models import Company, Order, Instrument, Portfolio, Account, Trade


######################################################
# Company
######################################################

class CompaniesRepo(ABC):
    @abstractmethod
    def get_company(self, id: int) -> Company:
        pass

    # @abstractmethod
    # def search_company(self, start_after: Optional[int] = None,
    #                 end_before: Optional[int] = None) -> List[Post]:
    #    pass

    # @abstractmethod
    # def count_posts(self) -> int:
    #    pass

    @abstractmethod
    def save(self, c: Company):
        pass

    @abstractmethod
    def update(self, c: Company):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class OrdersRepo(ABC):
    @abstractmethod
    def get_order(self, company_id: int) -> Order:
        pass

    # @abstractmethod
    # def search_company(self, start_after: Optional[int] = None,
    #                 end_before: Optional[int] = None) -> List[Post]:
    #    pass

    # @abstractmethod
    # def count_posts(self) -> int:
    #    pass

    @abstractmethod
    def save(self, o: Order):
        pass

    @abstractmethod
    def update(self, o: Order):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class InstrumentsRepo(ABC):
    @abstractmethod
    def get_instrument(self, instrument_id: int) -> Order:
        pass

    # @abstractmethod
    # def search_company(self, start_after: Optional[int] = None,
    #                 end_before: Optional[int] = None) -> List[Post]:
    #    pass

    # @abstractmethod
    # def count_posts(self) -> int:
    #    pass

    @abstractmethod
    def save(self, o: Instrument):
        pass

    @abstractmethod
    def update(self, o: Instrument):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class PortfoliosRepo(ABC):
    @abstractmethod
    def get_portfolio(self, portfolio_id: int) -> Portfolio:
        pass

    # @abstractmethod
    # def search_company(self, start_after: Optional[int] = None,
    #                 end_before: Optional[int] = None) -> List[Post]:
    #    pass

    # @abstractmethod
    # def count_posts(self) -> int:
    #    pass

    @abstractmethod
    def save(self, o: Portfolio):
        pass

    @abstractmethod
    def update(self, o: Portfolio):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class AccountsRepo(ABC):
    @abstractmethod
    def get_account(self, instrument_id: int) -> Order:
        pass

    # @abstractmethod
    # def search_company(self, start_after: Optional[int] = None,
    #                 end_before: Optional[int] = None) -> List[Post]:
    #    pass

    # @abstractmethod
    # def count_posts(self) -> int:
    #    pass

    @abstractmethod
    def save(self, o: Account):
        pass

    @abstractmethod
    def update(self, o: Account):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class TradesRepo(ABC):
    @abstractmethod
    def get_trade(self, instrument_id: int) -> Trade:
        pass

    # @abstractmethod
    def search_threads(self, start_after: Optional[int] = None,
                       end_before: Optional[int] = None) -> List[Trade]:
        pass

    # @abstractmethod
    def count_trades(self) -> int:
        pass

    @abstractmethod
    def save(self, o: Trade):
        pass

    @abstractmethod
    def update(self, o: Trade):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass
