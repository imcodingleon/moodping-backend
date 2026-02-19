from abc import ABC, abstractmethod
from typing import Optional

from account.domain.entity.account import Account


class AccountService(ABC):

    @abstractmethod
    def upsert_by_kakao(
        self,
        kakao_id: str,
        nickname: str | None,
        profile_image: str | None,
    ) -> Account:
        """카카오 로그인 시 사용자 조회/생성 또는 업데이트."""
        pass

    @abstractmethod
    def find_by_id(self, account_id: int) -> Optional[Account]:
        """ID로 계정 조회. 없으면 None 반환."""
        pass
