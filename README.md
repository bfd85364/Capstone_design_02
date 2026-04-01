# Capstone_design_02
캡스톤 디자인 작업물 02: RAG 파이프라인 구축 및 목업용 app 서버 구현 

--------------- 모듈 파일 및 주요 변수-------------

[혼용되는 용어]: vectorstore == vectorDB == Medic_INFO_DB 폴더 (전부 같은 표현이니 그냥 Medic_INFO_DB 폴더라고 생각해주세요)

[LLM-RAG 파이프라인]:
-llm.py: LLM-RAG의 가장 핵식점인 챗봇 기능을 위해 이식할 LLM 모델을 담고 있는 모듈입니다.
D_care_LLM() 모듈: 내부의 llm갹체를 통해 openrouter의  llm 모델을 자동으로 연결 시켜줍니다.
llm 객체 내의 model, api_key, model_kwargs 와 같은 요소들은 모두 그 값을 config.py에서 관리합니다.
(단,  변수로 반환하는 OR_API_KEY가 아니라 진짜 키값인  api_key는 env파일로 은닉중)

- llm_vectorstore.py: vectorstore(Medic_INFO_DB)를 구축하기 위한 모듈입니다. create_vectorstore 객체를 통해 pdf문서와 csv 문서의데이터를 얻어와 청크분활을 실시하고
허깅 페이스 임베딩 모델(한국어 처리에 특화된 임베딩 모델로 코사인 유사도 기법을 통해 질문자의 질문과 유사도가 가장 높은 답변을 생성해냄)을 통해 임베딩 모델을 불러온 후
vectorDB의 구축을 완료합니다. create_retriver 객체는 저장된 vector DB를 불러오는 기능을 합니다.
- embedding.py: 말그대로 csv문서와 pdf 문서를 임베딩 하는 모듈로 load_all_document를 통해 vectorDB에 임베딩할 문서들을 불러옵니다.
- llm_vectorstore_loader.py: vectorstore(Medic_INFO_DB)에 임베딩 되어 저장된 각각의 문서를 문서 타입별로 불러오는 기능을 하는 모듈입니다.
- llm_service.py: LLM-RAG의 QA 프롬프트 가이드의 영역에 해당하는 부분입니다.
동시에 부분적으로 어플리케이션에서 입력된 사용자정보를 프롬프트에 포함하여 답변시 반영하기
위한 모듈입니다. 주요 클래스로는 load_pdf(PyPDFLoader 모듈을 통해 PDF 문서 형태로 저장한 당뇨 의료 정보 문서를 가져옴) ,
load_text(TextLoader 모듈을 통해 메모장형식으로 저장된 데이터를 가져옴), load_csv(저장된 문서중 csv 형식의 데이터를 가져옴) 로 구성되어있습니다.

BASE_PROMPT = LLM 모델에게 챗봇 기능을 위해  일종의 역할을 부여하는 과정입니다, 현재 D-carebot에게
부여할 역할은 당뇨 관리를 돕는 헬스케어 챗봇입니다. 이에 맞추어 프롬프트를 설정하여 줍니다.

field_map = 이 부분이 사용자의 건강 정보 데이터를 프롬프트에 포함시키기 위한
필드입니다 (수집한 사용자의 건강 정보 데이터를 처리하는것은 app_schemas.py의 UserHealth 클래스를 호출하여
받아옵니다) , 현재 의료 도메인 전문가와의 상담 이전에 사용자로부터 입력 받을 기본 건강 정보 변수에 대한 논의가 마무리 되지 않은 관계로
임의로 "name"(이름), "age"(나이), "diabetes_type"(당뇨 유형 ), "fasting_glucose"(공복 혈당 수치), "hba1c"(당화혈색소 수치), "medications"(복용약물),
"allergies"(알레르기), "note"(기타 특이사항) 으로 정의 하였습니다.

---

[app 관련 모듈]:

- D_care_main.py: 전체 코드를 실행하기 위한 main 모듈로, 대다수의 모듈의 초기화가 해당 파일에서 이루어집니다.
- app_router.py: API 엔드게이트의 경로 설정을 위한 모듈입니다.
서버 통신과 관련된 부분으로 주요 변수로는 APIRouter()로 인스턴스와 엔드 포인트 등록에 사용됩니다. 이어서 주요 함수로는 root()를 통해
서버 상태가 안정적인지 확인하고, health() 함수를 통해 LLM 모델의 API의 초기화 상태가 정상적인지 확인합니다. 마지막으로 chat() 함수를 통해
챗봇의 메인 기능을 수행합니다.
- app_schemas.py: 해당 파일은 어플리케이션의 회원 가입 폼에서 수집한 사용자의 건강 정보 데이터를
입력 처리하기 위한 스키마입니다. 주요 클래스로는 UserHealth, ChatRequest, ChatResponse가 존재합니다.
- app_state.py: 서버 전체 영역을 공유하는 개체입니다. lifespan에서 초기화한 후 router를 참조합니다.

---

[config-설정관리]:
-config.py: 어플리케이션, OPENROUTER 게이트 연결에 필요한 API키, 포트 번호와 호스트 주소를 저장하는 파일입니다.

OR_API_KEY -> os.getenv를 통해 env 파일에 은닉된  OPEN ROUTER의 API키를 받아오는 변수입니다.

LLM_MODEL -> OPEN ROUTER에서 지원되는 LLM 모델을 선정 하여 가져오는 변수로 현재는 "openrouter/free"라고 명시하여
해당 모델들 중 자동으로 무료(free)인 모델만을 가져오도록 선정하였습니다.

LLM_IGNORE_PROVIDERS는 이런식으로 불러오는 API키중  민감 정보 유출 우려등의 이유로 보안상 연결을 꺼려하는 LLM 모델을 걸러주는
변수 입니다, 2025년 사용자 수집 정보의  사용처가 불분명한걸로  이슈가 있었던 LLM모델인 딥시크와 기타 관련 공급망은 차단해두었습니다.

FAISS_DB_PATH ->임베딩한 문서의 내용을  저장할 vector DB의 저장 경로를  의미합니다,
현재는 의료 도메인 정보를 저장한다는 의미로 생성한 Medic_INFO_DB  폴더를 저장경로로 지정하였습니다

EMBEDDING_MODEL -> 참고문서의 텍스트를 vector화 시켜주는 임베딩 모델을 의미합니다. 현재 사용중인 sentence-transformers를 사용하여 문장 또는 문단을
일정한 단위(청크)로 나누어 임베딩하는 모델입니다.
CHUNK_SIZE = 텍스트를 분활하는 단위입니다. 현재는최대 500자입니다.
CHUNK_OVERLAP = 인접한 청크 사이에 중복으로 포함할 문자의 수를 의미합니다.
현재는 최대 50자로 설정하였습니다.

HOST: 해당  서버의 호스트 주소를 의미
PORT: 해당 서버의 포트번호를  의미

RETRIVER객체는 검색기로서 사용자의 질문과 관련된 문서를 벡터 저장소에서 찾아내는
기능을 수행합니다. 여기서 RETRIVER_TOP_K =3는 검색 결과 중 상위 3개를 반환 한다는 의미입니다.

---

[현재 진행과정]

- (OpenRouter) LLM 연동 확인 (완료)
- RAG 파이프라인 구축 (완료) -> (3월 31일 Medic_INFO_DB에 문서 임베딩 실패하는 문제 발생 -> 4월 1일 조치 완료)
- FAST API를 활용한 서버 구축 + 라우터를 통한 OpenRouter API 엔드포인트(chat) 경로 설정 (완료)

[예상하는 다음 진행 사항]:

-의료 도메인 전문가 자문 이후 app_schema의 수집정보 변수 수정될것으로 예상함 

- 의료 도메인 정보 참고 문서 갱신(추가)시 -> Medic_INFO_DB 폴더 파일들 삭제후  embedding.py로 임베딩 재시작

-flutter 앱 ui 구상 (안드로이드 스튜디오 활용예정)
-어플케이션 테스트
-통합테스트
-버그 수정  (프롬프트 수정, 임베딩 도중 문제 발생시, 어플리케이션 호환성 문제 발생시)
