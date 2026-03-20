# 🏗️ Construction-Safety-AI: 2-Pass Generation 기반 건설 안전 RAG 시스템

## 📌 Project Overview
[cite_start]본 프로젝트는 **'한솔 데코 시즌3 생성 AI 경진대회'** 출품작으로, 건설 현장의 안전성을 강화하고 사고 예방 및 대응 체계를 고도화하기 위해 개발된 시스템입니다[cite: 137, 330]. [cite_start]사고 경위가 입력되면 지침서를 근거로 구체적인 행동 요령과 위험 예방 방법을 정확하게 출력하는 것을 목표로 설계되었습니다[cite: 332].

* [cite_start]**진행 기간:** 2025.02 ~ 2025.03 [cite: 132]
* [cite_start]**팀명 / 인원:** 1인 개발 (개인 프로젝트) [cite: 138]
* [cite_start]**주요 기술:** RAG, 2-Pass Generation, Prompt Engineering [cite: 139, 360]
* [cite_start]**결과:** 최종 12위 (24팀 중) [cite: 138]

## 🎯 Key Challenges & Solutions

### 1. 긴 컨텍스트 처리 시 발생하는 노이즈 제어
* [cite_start]**Problem:** 문서의 길이가 길어질수록 LLM의 답변에 불필요한 서론이나 부연 설명이 덧붙여지는 현상이 발생했습니다[cite: 355]. [cite_start]당시 가용한 로컬 한국어 LLM 중 대규모 토큰을 안정적으로 처리할 모델이 마땅치 않았습니다[cite: 356].
* [cite_start]**Solution:** 단일 생성 모델의 한계를 극복하기 위해 **2-Pass Generation** 아키텍처를 고안 및 도입했습니다[cite: 356].

### 2. 2-Pass Generation 파이프라인 구축
* [cite_start]**1st Pass:** `NCSOFT/Llama-VARCO-8B-Instruct` 모델과 QA Chain을 활용하여 답변의 초안을 우선적으로 생성했습니다[cite: 357].
* [cite_start]**2nd Pass:** `Qwen/Qwen2.5-14B-Instruct-1M` 모델에 1차 초안, 검색된 Context, 그리고 Baseline을 단일 프롬프트로 주입하여, 최종적으로 핵심만 담은 한 문장의 답변을 산출하도록 파이프라인을 구축했습니다[cite: 358, 359].

### 3. 모델 제어 및 프롬프트 엔지니어링
* [cite_start]**Problem:** LLM 고유의 말투나 학습 데이터에 포함된 텍스트 형식이 그대로 노출되는 등, 출력이 의도한 포맷으로 제어되지 않는 문제가 잦았습니다[cite: 361].
* [cite_start]**Solution:** 서문이나 배경 설명을 절대 포함하지 않게 하고, "제안합니다"와 같은 불필요한 문구를 금지하는 등 매우 엄격한 룰을 프롬프트에 적용하여 실질적이고 실행 가능한 답변만 도출되도록 제어했습니다[cite: 347, 348, 349, 351].

## 🛠️ Tech Stack & Environment
* [cite_start]**LLM (1st Pass):** `NCSOFT/Llama-VARCO-8B-Instruct` [cite: 357]
* [cite_start]**LLM (2nd Pass):** `Qwen/Qwen2.5-14B-Instruct-1M` [cite: 358]
* [cite_start]**Core Libraries:** Hugging Face, LangChain [cite: 158, 162]

## 💡 Lessons Learned
* [cite_start]**논문 리서치와 파이프라인 디벨롭:** 1인 개발이라는 부담감 속에서도, 관련 논문을 직접 찾아보고 2-Pass Generation 파이프라인을 직접 구현하며 개발의 성취감을 크게 느낄 수 있었습니다[cite: 366].
* [cite_start]**서비스 관점의 AI 제어:** 단순히 질문에 답하는 AI를 넘어, 사용자가 원하는 정확한 포맷으로 출력하도록 제어하는 '서비스 목적의 프롬프트 엔지니어링' 역량이 필수적임을 깨달았습니다[cite: 362].
* [cite_start]**실전 트러블슈팅:** 라이브러리 버전 충돌, API 연동 등 이론으로는 겪어보기 힘든 실전 환경의 이슈들을 디버깅하며 엔지니어로서의 기본기를 단단히 다졌습니다[cite: 369].
