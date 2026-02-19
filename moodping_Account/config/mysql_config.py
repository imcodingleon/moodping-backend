from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import get_settings


class MySQLConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        settings = get_settings()
        self._engine = create_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=self._engine,
        )
        self.Base = declarative_base()

    def get_engine(self):
        return self._engine

    def get_session(self):
        return self.SessionLocal()

    def get_base(self):
        return self.Base
