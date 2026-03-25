import os
import faiss
import pickle
import numpy as np
from tqdm import tqdm
from typing import List
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS as LangChainFAISS
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import (
    EMBEDDING_MODEL_ID,
    EMBEDDING_DIM,
    FAISS_INDEX_BUFFER_SIZE,
    FAISS_INDEX_PATH,
    FULL_TEXTS_PATH,
    PDF_DIR_PATH,
)
from src.pdf_processor import get_pdf_files, process_single_pdf


def _get_embedding_model() -> SentenceTransformer:
    """SentenceTransformer 임베딩 모델을 로드합니다."""
    print(f"임베딩 모델({EMBEDDING_MODEL_ID})을 로드합니다...")
    return SentenceTransformer(EMBEDDING_MODEL_ID)


def build_and_save_pdf_index():
    """
    PDF 파일들을 처리하여 FAISS 인덱스를 구축하고 파일로 저장합니다.
    이미 인덱스 파일이 존재하면 이 과정을 건너뜁니다.
    """
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FULL_TEXTS_PATH):
        print("이미 구축된 PDF 인덱스 파일이 존재합니다. 인덱스 생성을 건너뜁니다.")
        return

    print("PDF 기반 FAISS 인덱스 구축을 시작합니다...")
    model = _get_embedding_model()
    pdf_files = get_pdf_files(PDF_DIR_PATH)
    if not pdf_files:
        print(f"경고: '{PDF_DIR_PATH}'에서 PDF 파일을 찾을 수 없습니다. 인덱스 구축을 중단합니다.")
        return

    index = faiss.IndexHNSWFlat(EMBEDDING_DIM, FAISS_INDEX_BUFFER_SIZE)
    full_texts = []

    print(f"총 {len(pdf_files)}개의 PDF 파일을 처리합니다.")
    for pdf in tqdm(pdf_files, desc="PDF 처리 및 임베딩"):
        category = os.path.splitext(os.path.basename(pdf))[0]
        processed_chunks = process_single_pdf(pdf)

        for chunk in processed_chunks:
            full_text = f"카테고리: {category}, 내용: {chunk}"
            embedding = model.encode([full_text])[0].astype(np.float32)
            index.add(np.array([embedding]))
            full_texts.append(full_text)

    print(f"FAISS 인덱스를 '{FAISS_INDEX_PATH}' 경로에 저장합니다.")
    faiss.write_index(index, FAISS_INDEX_PATH)

    print(f"원본 텍스트를 '{FULL_TEXTS_PATH}' 경로에 저장합니다.")
    with open(FULL_TEXTS_PATH, "wb") as f:
        pickle.dump(full_texts, f)
    print("PDF 인덱스 구축 및 저장이 완료되었습니다.")


def get_qa_retriever(train_documents: List[str]):
    """
    주어진 훈련 문서(질문-답변 쌍)로부터 인-메모리 FAISS Retriever를 생성합니다.

    Args:
        train_documents (List[str]): "질문: [질문]
    답변: [답변]" 형식의 문서 리스트.

    Returns:
        FAISS retriever 객체.
    """
    print("질문-답변 데이터 기반의 FAISS Retriever를 생성합니다...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_ID)
    vector_store = LangChainFAISS.from_texts(train_documents, embeddings)
    print("Retriever 생성이 완료되었습니다.")
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
