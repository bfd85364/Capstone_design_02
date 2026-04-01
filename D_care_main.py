from contextlib import asynccontextmanager, contextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm import D_care_LLM
from llm_vectorstore import create_retriver
from app_router import router
import app_state

#main 파일 실행하기 전에 탐색기로 폴더 열기 들어가서  반드시 Medical_INFO_DB 폴더에 의료정보문서(index.faiss)와 피클파일(index.pkl)등이  존재하는지 확인 할것
#없으면 embedding.py 파일을 실행할것
# cd C:\Users\User\source\repos\D-care_01 이라고 입력 -> cd D-care_01 입력
#이후 가상환경 실행  -> env-Dcare01\Scripts\activate.bat 입력후 
#python embedding.py 입력


#목업 앱 기능 확인을 위해 서버 실행시 cmd창 열어서
#cd C:\Users\User\source\repos\D-care_01 이라고 입력 -> cd D-care_01 입력
# -> env-Dcare01\Scripts\activate.bat 입력후 
# uvicorn D_care_main:app --reload

# 챗봇 기능 테스트 하기 
# 서버 실행후 http://localhost:8000/docs 접속
# POST / chat -> Try it out -> Request body에 {"question": "당뇨에 대해 설명해줘"}에서 원하는 질문 입력 -> Execute 클릭

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("서버 초기화 중...")
    print("LLM 초기화 중...")
    app_state.llm = D_care_LLM()
    print("LLM 연결 완료")

    print("RAG 파이프라인 초기화 중...")
    app_state.retriever = create_retriver()
    if app_state.retriever:
        print("RAG 파이프라인 연결 완료")

    print("서버 준비 완료! http://localhost:8000")
    print("API 문서: http://localhost:8000/docs")

    yield

    print("서버 종료 중...")

app = FastAPI(
    title = "D-care_bot API",
    lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

