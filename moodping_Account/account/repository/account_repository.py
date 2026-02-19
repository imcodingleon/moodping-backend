from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session

from account.domain.entity.account import Account


class AccountRepository(ABC):

    @abstractmethod
    def find_by_kakao_id(self, session: Session, kakao_id: str) -> Optional[Account]:
        pass

    @abstractmethod
    def save(self, session: Session, account: Account) -> Account:
        pass

    @abstractmethod
    def find_by_id(self, session: Session, account_id: int) -> Optional[Account]:
        pass
