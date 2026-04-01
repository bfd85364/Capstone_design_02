from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import HumanMessage, SystemMessage
from app_schemas import UserHealth, ChatResponse

#해당 파일은 RAG 모듈의 QA 프롬프트 가이드 해당하는 부분(프롬프트 엔지니어링 영역)

BASE_PROMPT = ("당신은 당뇨 관리를 돕는 헬스케어 챗봇입니다."
               "사용자의 혈당,식단, 운동 관련 질문에 친절하고 정확하게 답변하세요."
               "의학적 진단은 하지 않으며, 전문의 상담을 권하도록 합니다.")

def create_system_prompt(user_health: UserHealth | None) -> str:
    if not user_health:
        return BASE_PROMPT

    # 회원가입 폼에서 수집한 사용자의 건강 정보 데이터를 프롬프트에 포함시키기 위한 필드 매핑
    field_map ={
        "name": ("이름", lambda v: v),
        "age": ("나이", lambda v: f"{v}세"),
        "diabetes_type": ("당뇨 유형", lambda v: f"{v}형 당뇨"),
        "fasting_glucose": ("공복 혈당 수치", lambda v: f"{v} mg/dL"),
        "hba1c": ("당화혈색소 수치", lambda v: f"{v}%"),
        "medications": ("복용 중인 약물 목록", lambda v: ",".join(v) if v else None),
        "allergies": ("알레르기 정보", lambda v: ",".join(v) if v else None),
        "notes": ("추가 정보나 메모", lambda v: v if v else None)
        }
    
    health_lines = ["\n\n사용자의 건강 정보: "]
    for field, (label, formatter) in field_map.items():
        value = getattr(user_health, field, None)
        formatted = formatter(value) if value is not None else None
        if formatted:
            health_lines.append(f"- {label}: {formatted}")

    health_lines.append("\n 위 환자 정보를 참고하여 개인화 된 답변을 제공하시오.")
    return BASE_PROMPT + "".join(health_lines)

def run_chat(
    llm: ChatOpenRouter,
    retriever,
    question: str,
    user_health: UserHealth | None
    ) -> ChatResponse:
    system_prompt = create_system_prompt(user_health)
    rag_used = False

    if retriever:
        related_docs = retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in related_docs])
        system_prompt += f"\n\n참고 의료 데이터:\n{context}"
        rag_used = True

    message = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question),
    ]
    response = llm.invoke(message) 
    return ChatResponse(answer=response.content, rag_used=rag_used)

