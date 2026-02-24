"""
MoodAnalysisController — FastAPI 라우터.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from moodping.config.mysql_config import get_db
# authentication에서 구현할 get_current_user_payload
# from moodping.authentication.controller.authentication_controller import get_current_user_payload
from moodping.mood_record.domain.entity.mood_record import MoodRecord
from moodping.mood_analysis.service.mood_analysis_service_impl import MoodAnalysisServiceImpl

mood_analysis_router = APIRouter(prefix="/mood-analysis", tags=["mood-analysis"])

def inject_mood_analysis_service() -> MoodAnalysisServiceImpl:
    return MoodAnalysisServiceImpl.get_instance()

@mood_analysis_router.post("/{record_id}/analyze")
async def analyze_record(
    record_id: int,
    db: Session = Depends(get_db),
    # current_user_payload: dict = Depends(get_current_user_payload),
    service: MoodAnalysisServiceImpl = Depends(inject_mood_analysis_service),
):
    record: MoodRecord | None = db.get(MoodRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"MoodRecord(id={record_id})를 찾을 수 없습니다.")

    result = await service.analyze_and_save(record=record, db=db)
    if result is None:
        raise HTTPException(status_code=502, detail="LLM 분석에 실패했습니다. 잠시 후 다시 시도해 주세요.")

    return {
        "record_id": record_id,
        "analysis_text": result.analysis_text,
    }

@mood_analysis_router.get("/{record_id}")
async def get_analysis(
    record_id: int,
    db: Session = Depends(get_db),
    service: MoodAnalysisServiceImpl = Depends(inject_mood_analysis_service),
):
    result = await service.get_analysis_by_record_id(record_id=record_id, db=db)
    if result is None:
        raise HTTPException(status_code=404, detail=f"record_id={record_id} 에 대한 분석 결과가 없습니다.")

    return {
        "record_id": record_id,
        "analysis_text": result.analysis_text,
    }
