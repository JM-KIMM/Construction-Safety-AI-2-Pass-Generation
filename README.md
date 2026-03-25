# 건설 현장 안전사고 재발 방지 대책 생성 RAG 에이전트

## 📝 프로젝트 설명

이 프로젝트는 건설 현장에서 발생한 안전사고 데이터를 기반으로, 유사한 사고의 재발을 방지하기 위한 대책 및 향후 조치 계획을 자동으로 생성하는 RAG(Retrieval-Augmented Generation) 기반의 AI 에이전트입니다.

사용자가 사고 관련 정보(공사 종류, 사고 원인, 작업 프로세스 등)를 입력하면, 에이전트는 과거 유사 사고 사례 데이터를 검색하여 가장 적절한 재발 방지 대책을 생성합니다. 이 과정에서 Hugging Face의 `NCSOFT/Llama-VARCO-8B-Instruct` 모델이 활용됩니다.

## ✨ 주요 기능

- **데이터 기반 답변 생성:** 실제 `train.csv`의 사고 사례를 기반으로 답변을 생성합니다.
- **RAG 파이프라인:** LangChain을 활용하여 FAISS 벡터 스토어에서 효율적으로 관련 정보를 검색하고, Hugging Face의 언어 모델(LLM)을 통해 자연스러운 문장을 생성합니다.
- **PDF 문서 처리:** `건설안전지침` PDF 파일들을 벡터화하여, 법규 및 지침에 기반한 답변을 생성할 수 있는 기반을 마련합니다. (현재는 QA 데이터 기반 Retriever 사용)
- **모듈화된 구조:** `src` 폴더 내에 데이터 로딩, 전처리, 모델 관리, RAG 체인 등의 기능이 모듈별로 깔끔하게 정리되어 유지보수와 확장이 용이합니다.
- **2-Pass Generation 파이프라인:** 1차로 `NCSOFT/Llama-VARCO-8B-Instruct` 모델을 사용하여 답변 초안을 생성하고, 2차로 `Qwen/Qwen2.5-14B-Instruct-1M` 모델이 초안과 검색된 컨텍스트를 기반으로 최종 핵심 답변을 생성합니다. 이를 통해 긴 컨텍스트 처리 시 발생하는 노이즈를 제어하고 답변의 정확도를 높입니다.

## 📂 프로젝트 구조

```
.
├── data/                  # CSV, PDF 등 데이터 파일 위치
├── src/                   # 소스 코드
│   ├── config.py          # 설정 변수 (모델 ID, 경로 등)
│   ├── data_loader.py     # 데이터 로드 및 전처리
│   ├── model_loader.py    # Hugging Face 모델 및 파이프라인 로드
│   ├── pdf_processor.py   # PDF 문서 처리 및 텍스트 추출
│   ├── rag_chain.py       # RAG QA 체인 생성
│   └── vector_store.py    # FAISS 벡터 DB 구축 및 관리
├── main.py                # 메인 실행 스크립트
├── requirements.txt       # 필요 라이브러리 목록
├── .gitignore             # Git 추적 제외 목록
└── README.md              # 프로젝트 설명 파일
```

## 🛠️ 설치 및 실행 방법

### 1. 프로젝트 복제 (선택 사항)

만약 이 프로젝트를 GitHub에 올렸다면, 아래 명령어로 복제합니다.
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. 환경 설정

- **데이터 파일**: `train.csv`, `test.csv` 및 `건설안전지침` PDF 폴더를 `data/` 디렉터리 안에 넣어주세요.
- **API 토큰**: 프로젝트 루트에 `.env` 파일을 생성하고, Hugging Face Hub API 토큰을 아래 형식으로 추가합니다.
  ```
  HF_TOKEN="여기에_huggingface_토큰을_붙여넣으세요"
  ```

### 3. 가상환경 생성 및 라이브러리 설치

```powershell
# 1. 파이썬 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화 (Windows)
.\venv\Scripts\activate
# (macOS/Linux의 경우: source venv/bin/activate)

# 3. 필요 라이브러리 설치
pip install -r requirements.txt
```

### 4. 프로젝트 실행

아래 명령어를 실행하여 답변 생성을 시작합니다. 최종 결과는 프로젝트 루트에 `submission.csv` 파일로 저장됩니다.

```bash
python main.py
```
**주의:** 최초 실행 시 LLM 모델 다운로드, 데이터 처리 등으로 인해 시간이 매우 오래 걸릴 수 있으며, 높은 사양의 GPU가 필요할 수 있습니다.

## ⚙️ 주요 기술 스택

- Python 3.x
- PyTorch
- Hugging Face LLMs:
  - `NCSOFT/Llama-VARCO-8B-Instruct (1st Pass)`
  - `Qwen/Qwen2.5-14B-Instruct-1M (2nd Pass)`
- LangChain, Transformers, Sentence-Transformers
- FAISS (Facebook AI Similarity Search)
- Pandas, NumPy
- Kiwipiepy (한국어 형태소 분석기)
- PyMuPDF
