from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from account.controller.account_controller import account_router
from config.mysql_config import MySQLConfig
from config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="MoodPing API",
    description="MoodPing 백엔드 - 도메인 분리 아키텍처",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router)

# MP-04 완료 후 추가 예정
# app.include_router(authentication_router)

# MP-05 완료 후 추가 예정
# app.include_router(kakao_authentication_router)

# MP-02 완료 후 추가 예정
# app.include_router(mood_record_router)

# MP-03 완료 후 추가 예정
# app.include_router(event_log_router)

# MP-06 완료 후 추가 예정
# app.include_router(mood_analysis_router)

# MP-07 완료 후 추가 예정
# app.include_router(weekly_report_router)


if __name__ == "__main__":
    import uvicorn

    Base = MySQLConfig().get_base()
    engine = MySQLConfig().get_engine()
    Base.metadata.create_all(bind=engine)

    uvicorn.run(app, host="0.0.0.0", port=33333)
