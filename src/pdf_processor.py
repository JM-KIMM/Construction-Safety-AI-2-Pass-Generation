import os
import re
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from src.utils import clean_text, apply_spacing_correction
from src.config import PDF_DIR_PATH

def remove_unwanted_pages(docs: List) -> List:
    """
    문서 리스트에서 "목차", "정의", "부록" 등 특정 키워드가 포함된 페이지를 제거합니다.

    Args:
        docs (List): LangChain의 `Document` 객체 리스트.

    Returns:
        List: 필터링된 `Document` 객체 리스트.
    """
    unwanted_page_patterns = re.compile(r"(목차|목 차|정의|부록|별지|별표|개정)")
    return [doc for doc in docs if not unwanted_page_patterns.search(doc.page_content)]

def get_pdf_files(folder_path: str = PDF_DIR_PATH) -> List[str]:
    """
    지정된 디렉터리에서 모든 PDF 파일의 전체 경로를 찾아 리스트로 반환합니다.

    Args:
        folder_path (str): PDF 파일이 있는 디렉터리 경로.

    Returns:
        List[str]: PDF 파일 경로들의 리스트.
    """
    if not os.path.isdir(folder_path):
        print(f"경고: '{folder_path}' 디렉터리를 찾을 수 없습니다. 빈 리스트를 반환합니다.")
        return []
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(".pdf")]

def process_single_pdf(pdf_path: str) -> List[str]:
    """
    단일 PDF 파일을 처리하여 정제된 텍스트 덩어리(chunk)의 리스트를 생성합니다.

    - 불필요한 페이지 제거
    - 텍스트 정제 (기호, 번호 제거)
    - "KOSHA GUIDE" 기준으로 분할
    - 짧은 텍스트 병합
    - 띄어쓰기 및 맞춤법 교정

    Args:
        pdf_path (str): 처리할 PDF 파일의 경로.

    Returns:
        List[str]: 처리된 텍스트 덩어리(chunk)의 리스트.
    """
    if not os.path.exists(pdf_path):
        print(f"경고: '{pdf_path}' 파일을 찾을 수 없습니다. 빈 리스트를 반환합니다.")
        return []

    # 1. PyMuPDFLoader로 PDF 로드
    docs = PyMuPDFLoader(pdf_path).load()

    # 2. 목차 등 불필요한 페이지 제거
    docs = remove_unwanted_pages(docs[2:])

    # 3. 전체 텍스트 추출 및 기본 정제
    pdf_text = " ".join(clean_text(doc.page_content) for doc in docs)

    # 4. "KOSHA GUIDE" 기준으로 텍스트 분할 및 메타데이터 제거
    chunks = re.split(r'(?i)KOSHA GUIDE', pdf_text)
    cleaned_chunks = [" ".join(chunk.strip().split()[9:]) for chunk in chunks if chunk.strip()]

    # 5. 짧은(270자 이하) 텍스트 덩어리를 이전 덩어리와 병합
    merged_chunks = []
    for chunk in cleaned_chunks:
        if merged_chunks and len(chunk.strip()) <= 270:
            merged_chunks[-1] += " " + chunk.strip()
        else:
            merged_chunks.append(chunk.strip())

    # 6. 각 텍스트 덩어리에 대해 띄어쓰기 교정 적용
    return [apply_spacing_correction(chunk) for chunk in merged_chunks if chunk]
