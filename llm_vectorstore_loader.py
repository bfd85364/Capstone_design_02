import json
import os
import re
from fastapi import File
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

def load_pdf(file_path: str) -> list[Document]:
    if not os.path.exists(file_path):
        print(f"파일 경로에 {file_path}이 존재하지 않습니다.")
        return []

    loader = PyPDFLoader(file_path)
    return loader.load()

def load_text(file_path: str) -> list[Document]:
    loader = TextLoader(file_path, encoding="utf-8")
    return loader.load()

def load_csv(file_path: str, rows_per_chunk: int = 1) -> list[Document]:
    if not os.path.exists(file_path):
        print(f"파일 경로에 {file_path}이 존재하지 않습니다.")
        return []

    df = pd.read_csv(file_path)
    documents = []
    
    for i in range(0, len(df), rows_per_chunk):
        chunk_df = df.iloc[i:i+rows_per_chunk] 
        row_lines = []
        for _, row in chunk_df.iterrows():
            row_text = ", ".join([f"{col}: {val}" for col, val in row.items()])
            row_lines.append(row_text)

        content = "\n".join(row_lines)
        documents.append(Document(page_content=content, metadata={"source": file_path, "rows": f"{i}~{i + len(chunk_df) - 1}"}))
        
    return documents

def load_json(file_path: str) -> list[Document]:
    if not os.path.exists(file_path):
        print(f"파일 경로에 {file_path}이 존재하지 않습니다.")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    if isinstance(data, list):
        for item in data:
            content = json.dumps(item, ensure_ascii=False, indent=2)
            documents.append(Document(page_content=content, metadata={"source": file_path}))
    else:
        content = json.dumps(data, ensure_ascii=False, indent=2)
        documents.append(Document(page_content=content, metadata={"source": file_path}))
    return documents

def load_all_documents(file_paths: list[str]) -> list[Document]:
    loaders = {
        ".pdf": load_pdf,
        ".txt": load_text,
        ".csv": load_csv,
        ".json": load_json,
    }

    all_docs = []
    for path in file_paths:
        ext = os.path.splitext(path)[-1].lower()
        print(f"파일 로드 중: {path}")
        loader_fn = loaders.get(ext)
        if loader_fn:
            all_docs.extend(loader_fn(path))
        else:
            print(f"지원하지 않는 파일 형식: {ext} - {path}") 
    return all_docs

