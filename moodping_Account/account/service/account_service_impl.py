from typing import Optional

from account.domain.entity.account import Account
from account.repository.account_repository_impl import AccountRepositoryImpl
from account.service.account_service import AccountService
from config.mysql_config import MySQLConfig


class AccountServiceImpl(AccountService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.account_repository = AccountRepositoryImpl.get_instance()
        return cls.__instance

    @classmethod
    def get_instance(cls) -> "AccountServiceImpl":
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def upsert_by_kakao(
        self,
        kakao_id: str,
        nickname: str | None,
        profile_image: str | None,
    ) -> Account:
        session = MySQLConfig().get_session()
        try:
            account = self.account_repository.find_by_kakao_id(session, kakao_id)

            if account:
                account.nickname = nickname
                account.profile_image = profile_image
            else:
                account = Account.create(
                    kakao_id=kakao_id,
                    nickname=nickname,
                    profile_image=profile_image,
                )
                self.account_repository.save(session, account)

            session.commit()

            # Eager load: 세션 닫기 전에 필드를 미리 읽어둠
            _ = account.id
            _ = account.kakao_id
            _ = account.nickname
            _ = account.profile_image

            return account

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def find_by_id(self, account_id: int) -> Optional[Account]:
        session = MySQLConfig().get_session()
        try:
            account = self.account_repository.find_by_id(session, account_id)

            if account:
                _ = account.id
                _ = account.kakao_id
                _ = account.nickname
                _ = account.profile_image

            return account

        finally:
            session.close()
