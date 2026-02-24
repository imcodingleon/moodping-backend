import json
import logging
import re
from sqlalchemy.orm import Session

from moodping.mood_record.domain.entity.mood_record import MoodRecord
from moodping.mood_analysis.service.mood_analysis_service import MoodAnalysisService, AnalysisResult
# llm client
from moodping.llm.factory import get_llm_client
from moodping.mood_analysis.domain.entity.mood_analysis import MoodAnalysis
from moodping.mood_analysis.prompt import mood_analysis_prompt
from moodping.mood_analysis.repository.mood_analysis_repository_impl import MoodAnalysisRepositoryImpl

logger = logging.getLogger(__name__)
_MAX_ANALYSIS_CHARS = 1500

class MoodAnalysisServiceImpl(MoodAnalysisService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls) -> "MoodAnalysisServiceImpl":
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.mood_analysis_repository = MoodAnalysisRepositoryImpl.get_instance()

    async def analyze_and_save(self, record: MoodRecord, db: Session) -> AnalysisResult | None:
        llm = get_llm_client()
        system_prompt = mood_analysis_prompt.SYSTEM_PROMPT
        user_prompt   = mood_analysis_prompt.build(record)

        raw = await llm.complete(system_prompt, user_prompt)
        if not raw:
            return None

        analysis_text = self._parse_analysis_text(raw)
        if not analysis_text:
            return None

        owner_id = record.user_id or record.anon_id

        try:
            analysis = MoodAnalysis.create(
                record_id=record.id,
                user_id=owner_id,
                analysis_text=analysis_text,
            )
            self.mood_analysis_repository.save(db, analysis)
            db.commit()
            return AnalysisResult(analysis_text=analysis_text)
        except Exception as exc:
            db.rollback()
            return None

    async def get_analysis_by_record_id(self, record_id: int, db: Session) -> AnalysisResult | None:
        analysis = self.mood_analysis_repository.find_by_record_id(db, record_id)
        if not analysis or not analysis.analysis_text:
            return None
        return AnalysisResult(analysis_text=analysis.analysis_text)

    @staticmethod
    def _parse_analysis_text(content: str) -> str | None:
        if not content:
            return None
        match = re.search(r'"analysis_text"\s*:\s*"((?:[^"\\]|\\.)*)"', content, re.DOTALL)
        if not match:
            match = re.search(r'"analysis_text"\s*:\s*"((?:[^"\\]|\\.)*)', content, re.DOTALL)
        if match:
            raw = match.group(1)
            text = raw.replace("\\n", "\n").replace('\\"', '"').replace("\\\\", "\\")
            return text[:_MAX_ANALYSIS_CHARS] if text.strip() else None

        try:
            cleaned = re.sub(r"```(?:json)?\s*", "", content, flags=re.IGNORECASE)
            cleaned = re.sub(r"```\s*$", "", cleaned, flags=re.MULTILINE).strip()
            data = json.loads(cleaned)
            text = data.get("analysis_text", "")
            return text[:_MAX_ANALYSIS_CHARS] if text.strip() else None
        except (json.JSONDecodeError, AttributeError):
            return content[:_MAX_ANALYSIS_CHARS]
