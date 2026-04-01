from langchain_openrouter import ChatOpenRouter
from config import OR_API_KEY, LLM_MODEL, LLM_IGNORE_PROVIDERS

def D_care_LLM() -> ChatOpenRouter:
    """ChatOpenRouter LLM 객체를 생성하고 반환"""
 
    if not OR_API_KEY:
        raise RuntimeError("OR_API_KEY가 없습니다. .env 파일을 확인하세요.")
 
    llm = ChatOpenRouter(
        model=LLM_MODEL,
        api_key=OR_API_KEY,
        model_kwargs={
            "provider": {
                "ignore": LLM_IGNORE_PROVIDERS
            }
        }
    )
    return llm