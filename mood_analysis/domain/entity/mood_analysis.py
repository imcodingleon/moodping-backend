"""
MoodAnalysis 도메인 엔터티.
"""
from sqlalchemy import BigInteger, Column, String, Text, DateTime
from sqlalchemy.sql import func
from moodping.config.mysql_config import Base

class MoodAnalysis(Base):
    __tablename__ = "mood_analysis"
    __table_args__ = {"extend_existing": True}

    id            = Column(BigInteger, primary_key=True, autoincrement=True)
    record_id     = Column(BigInteger, nullable=False, index=True)
    user_id       = Column(String(100), nullable=True)
    analysis_text = Column(Text, nullable=True)
    created_at    = Column(DateTime, nullable=False, server_default=func.now())

    @classmethod
    def create(
        cls,
        record_id: int,
        user_id: str | None,
        analysis_text: str,
    ) -> "MoodAnalysis":
        if not analysis_text or not analysis_text.strip():
            raise ValueError("analysis_text must not be empty")

        return cls(
            record_id=record_id,
            user_id=user_id,
            analysis_text=analysis_text.strip(),
        )
