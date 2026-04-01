import os
from langchain_community.document_loaders import pdf
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from config import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, RETRIVER_TOP_K, FAISS_DB_PATH

#해당 vectorstore객체에서 config.py에서 EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, RETRIVER_TOP_K, FAISS_DB_PATH를 가져옵니다.
def create_vectorstore(documents: list[Document]) -> FAISS:
    pdf_docs = [doc for doc in documents if doc.metadata.get("source", "").lower().endswith(".pdf")]
    csv_docs = [doc for doc in documents if doc.metadata.get("source", "").lower().endswith(".csv")]

    chunks = []

    if pdf_docs:
        pdf_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP,
            )
        
        pdf_chunks = pdf_splitter.split_documents(pdf_docs)
        chunks.extend(pdf_chunks)
        print("청크 분활 완료 갯수:", {len(chunks)})

    if csv_docs:
        chunks.extend(csv_docs)
        print(f"CSV 청크 수: {len(csv_docs)}")

    print("총 청크 수:", len(chunks))

    print("임베딩 모델 로드 중...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("vector DB 구축 완료")

    vectorstore.save_local(FAISS_DB_PATH)
    print("vector DB 저장 완료:", FAISS_DB_PATH)

    return vectorstore

def create_retriver():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    if not os.path.exists(FAISS_DB_PATH):
        print("파일 경로에 의료정보문서 혹은 DB폴더가 존재하지 않습니다.")
        return None

    print("vector DB 로드 중...")
    vectorstore = FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    print("vector DB 로드 완료")
    return vectorstore.as_retriever(search_kwargs={"k": RETRIVER_TOP_K})







            
