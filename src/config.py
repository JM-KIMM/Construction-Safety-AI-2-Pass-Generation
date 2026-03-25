import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 불러옵니다.
# 프로젝트 루트에 .env 파일을 만들고 HF_TOKEN="your_hf_token" 형식으로 저장하세요.
load_dotenv()

# Hugging Face Hub API 토큰
HF_TOKEN = os.getenv("HF_TOKEN")

# 모델 ID
EMBEDDING_MODEL_ID = "jhgan/ko-sbert-nli"
INITIAL_MODEL_ID = "NCSOFT/Llama-VARCO-8B-Instruct"
REFINE_MODEL_ID = "Qwen/Qwen2.5-14B-Instruct-1M"

# 파일 및 디렉터리 경로
DATA_DIR = "data"
SRC_DIR = "src"
TRAIN_CSV_PATH = os.path.join(DATA_DIR, "train.csv")
TEST_CSV_PATH = os.path.join(DATA_DIR, "test.csv")
PDF_DIR_PATH = os.path.join(DATA_DIR, "건설안전지침")
FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss_index.bin")
FULL_TEXTS_PATH = os.path.join(DATA_DIR, "full_texts.pkl")
SUBMISSION_PATH = "submission.csv"

# FAISS 벡터 저장소 설정
EMBEDDING_DIM = 768
FAISS_INDEX_BUFFER_SIZE = 32

# 모델 생성 파라미터
INITIAL_MODEL_MAX_NEW_TOKENS = 128
REFINE_MODEL_MAX_NEW_TOKENS = 64
MODEL_TEMPERATURE = 0.1
MODEL_TOP_P = 0.3
