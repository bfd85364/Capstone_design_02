from ftplib import all_errors
from pydantic import BaseModel
#해당 파일은 어플리케이션의 회원가입폼에서 수집한 사용자의 건강 정보 데이터를 처리하기 위한 스키마임

class UserHealth(BaseModel):
    name: str = "사용자"
    age: int | None = None
    diabetes_type: int | None = None  #당뇨 유형 1, 2, 기타
    fasting_glucose: float | None = None # 공복 혈당 수치
    hba1c: float | None = None #당화혈색소 수치
    medications: list[str] | None = None #복용 중인 약물 목록
    allergies: list[str] | None = None #알레르기 정보
    notes: str | None = None #추가 정보나 메모

class ChatRequest(BaseModel):
    question: str
    user_helth: UserHealth | None = None

class ChatResponse(BaseModel):
    answer: str
    rag_used: bool
