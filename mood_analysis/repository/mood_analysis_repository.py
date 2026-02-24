from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from moodping.mood_analysis.domain.entity.mood_analysis import MoodAnalysis

class MoodAnalysisRepository(ABC):
    @abstractmethod
    def save(self, session: Session, analysis: MoodAnalysis) -> MoodAnalysis:
        pass

    @abstractmethod
    def find_by_record_id(self, session: Session, record_id: int) -> MoodAnalysis | None:
        pass

    @abstractmethod
    def find_all_by_user_id(self, session: Session, user_id: str) -> list[MoodAnalysis]:
        pass

    @abstractmethod
    def exists_by_record_id(self, session: Session, record_id: int) -> bool:
        pass
