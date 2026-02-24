"""
MoodAnalysisService — 추상 베이스 클래스 (ABC).
"""
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from moodping.mood_record.domain.entity.mood_record import MoodRecord

class AnalysisResult:
    def __init__(self, analysis_text: str):
        self.analysis_text = analysis_text

class MoodAnalysisService(ABC):
    @abstractmethod
    async def analyze_and_save(
        self,
        record: MoodRecord,
        db: Session,
    ) -> AnalysisResult | None:
        pass

    @abstractmethod
    async def get_analysis_by_record_id(
        self,
        record_id: int,
        db: Session,
    ) -> AnalysisResult | None:
        pass
