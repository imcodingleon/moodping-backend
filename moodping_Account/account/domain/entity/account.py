from sqlalchemy import BigInteger, Column, String, DateTime
from sqlalchemy.sql import func

from config.mysql_config import MySQLConfig

Base = MySQLConfig().get_base()


class Account(Base):
    __tablename__ = "account"

    id            = Column(BigInteger, primary_key=True, autoincrement=True)
    kakao_id      = Column(String(100), nullable=False, unique=True)
    nickname      = Column(String(100), nullable=True)
    profile_image = Column(String(500), nullable=True)
    created_at    = Column(DateTime, nullable=False, server_default=func.now())
    updated_at    = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    @classmethod
    def create(cls, kakao_id: str, nickname: str | None = None, profile_image: str | None = None) -> "Account":
        if not kakao_id or not kakao_id.strip():
            raise ValueError("kakao_id는 필수 값입니다.")

        if nickname is not None and len(nickname) > 100:
            raise ValueError("nickname은 100자를 초과할 수 없습니다.")

        if profile_image is not None and len(profile_image) > 500:
            raise ValueError("profile_image URL은 500자를 초과할 수 없습니다.")

        return cls(
            kakao_id=kakao_id.strip(),
            nickname=nickname,
            profile_image=profile_image,
        )
