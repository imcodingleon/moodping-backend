from sqlalchemy.orm import Session
from moodping.mood_analysis.domain.entity.mood_analysis import MoodAnalysis
from moodping.mood_analysis.repository.mood_analysis_repository import MoodAnalysisRepository

class MoodAnalysisRepositoryImpl(MoodAnalysisRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls) -> "MoodAnalysisRepositoryImpl":
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save(self, session: Session, analysis: MoodAnalysis) -> MoodAnalysis:
        session.add(analysis)
        return analysis

    def find_by_record_id(self, session: Session, record_id: int) -> MoodAnalysis | None:
        return session.query(MoodAnalysis).filter(MoodAnalysis.record_id == record_id).first()

    def find_all_by_user_id(self, session: Session, user_id: str) -> list[MoodAnalysis]:
        return session.query(MoodAnalysis).filter(MoodAnalysis.user_id == user_id).order_by(MoodAnalysis.created_at.desc()).all()

    def exists_by_record_id(self, session: Session, record_id: int) -> bool:
        return session.query(MoodAnalysis).filter(MoodAnalysis.record_id == record_id).count() > 0
