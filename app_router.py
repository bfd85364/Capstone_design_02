from math import e
from fastapi import APIRouter, HTTPException
from app_schemas import ChatRequest, ChatResponse
from llm_service import run_chat
import app_state

router = APIRouter()

@router.get("/")
async def root():
    return{
        "status": "running",
        "rag_enabled": app_state.retriever is not None
        }

@router.get("/health")
async def health():
    return {
        "status": "안정",
        "llm": app_state.llm is not None,
        "rag": app_state.retriever is not None,
        }

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if app_state.llm is None:
        raise HTTPException(status_code=503, detail="LLM이 초기화되지 않았습니다.")

    try:
        return run_chat(
            llm=app_state.llm,
            retriever=app_state.retriever,
            question=request.question,
            user_health=request.user_helth
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"챗봇 응답 생성 중 오류 발생: {str(e)}")