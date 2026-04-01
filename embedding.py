from fastapi.background import P
from llm_vectorstore import create_vectorstore
from llm_vectorstore_loader import load_all_documents
from config import DATA_FILES

# cd C:\Users\User\source\repos\D-care_01 이라고 입력 -> cd D-care_01 입력
# 이후 가상환경 실행-> env-Dcare01\Scripts\activate.bat 입력후 
#python embedding.py 입력

print("문서 로드 중...")
documents = load_all_documents(DATA_FILES)
print(f"총 {len(documents)}개의 문서 로드 완료")

print("vector DB에 임베딩 문서 저장중")
create_vectorstore(documents)
print("완료")
