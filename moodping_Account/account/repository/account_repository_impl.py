from typing import Optional

from sqlalchemy.orm import Session

from account.domain.entity.account import Account
from account.repository.account_repository import AccountRepository


class AccountRepositoryImpl(AccountRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls) -> "AccountRepositoryImpl":
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_by_kakao_id(self, session: Session, kakao_id: str) -> Optional[Account]:
        return (
            session.query(Account)
            .filter(Account.kakao_id == kakao_id)
            .first()
        )

    def save(self, session: Session, account: Account) -> Account:
        session.add(account)
        return account

    def find_by_id(self, session: Session, account_id: int) -> Optional[Account]:
        return (
            session.query(Account)
            .filter(Account.id == account_id)
            .first()
        )
