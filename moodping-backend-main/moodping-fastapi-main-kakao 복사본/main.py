from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.mysql_config import MySQLConfig
from config.settings import get_settings

# ── 도메인 라우터 ─────────────────────────────────────────────
# MP-01 완료 후 활성화
# from account.controller.account_controller import account_router

# MP-04 완료 후 활성화
# from authentication.controller.authentication_controller import authentication_router

# MP-05 완료 후 활성화
# from kakao_authentication.controller.kakao_authentication_controller import kakao_authentication_router

# MP-02 완료 후 활성화
# from mood_record.controller.mood_record_controller import mood_record_router

# MP-03 완료 후 활성화
# from event_log.controller.event_log_controller import event_log_router

# MP-06 완료 후 활성화
# from mood_analysis.controller.mood_analysis_controller import mood_analysis_router

# MP-07 ✅
from weekly_report.controller.weekly_report_controller import weekly_report_router

# ─────────────────────────────────────────────────────────────

settings = get_settings()

app = FastAPI(
    title="MoodPing API",
    description="MoodPing 감정 기록 백엔드",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 라우터 등록 ───────────────────────────────────────────────
# app.include_router(kakao_authentication_router)
# app.include_router(account_router)
# app.include_router(authentication_router)
# app.include_router(mood_record_router)
# app.include_router(event_log_router)
# app.include_router(mood_analysis_router)
app.include_router(weekly_report_router)
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    Base = MySQLConfig().get_base()
    engine = MySQLConfig().get_engine()
    Base.metadata.create_all(bind=engine)

    uvicorn.run(app, host="0.0.0.0", port=33333)
