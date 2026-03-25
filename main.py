import pandas as pd
from tqdm import tqdm

from src.config import SUBMISSION_PATH
from src.data_loader import get_prepared_data, create_training_documents, create_test_questions
from src.vector_store import get_qa_retriever
from src.model_loader import load_initial_model_and_tokenizer
from src.rag_chain import create_qa_chain

def main():
    """
    전체 RAG 파이프라인을 실행하는 메인 함수입니다.
    데이터 로딩, 전처리, 모델 로딩, 답변 생성 및 저장까지의 과정을 조율합니다.
    """
    # 1. 데이터 로드 및 전처리
    train_df, test_df = get_prepared_data()
    if train_df is None or test_df is None:
        print("데이터 로드에 실패하여 프로그램을 종료합니다.")
        return

    # 2. 훈련 데이터를 사용하여 Retriever 생성
    train_documents = create_training_documents(train_df)
    qa_retriever = get_qa_retriever(train_documents)

    # 3. 모델 및 QA 체인 로드
    initial_pipeline, _ = load_initial_model_and_tokenizer()
    qa_chain = create_qa_chain(initial_pipeline, qa_retriever)

    # 4. 테스트 질문 리스트 생성
    test_questions = create_test_questions(test_df)

    # 5. 각 테스트 질문에 대해 답변 생성
    print(f"총 {len(test_questions)}개의 테스트 데이터에 대한 답변 생성을 시작합니다...")
    results = []
    for question in tqdm(test_questions, desc="답변 생성 중"):
        try:
            response = qa_chain.invoke({"query": question})
            answer = response.get('result', '생성된 답변 없음')
            results.append(answer.strip())
        except Exception as e:
            print(f"질문 처리 중 오류 발생: {question}오류: {e}")
            results.append("오류 발생")

    # 6. 결과(submission) 저장
    print("답변 생성이 완료되었습니다. 제출 파일을 생성합니다...")
    
    # test.csv에서 'ID' 컬럼을 가져와서 결과와 병합
    submission_df = test_df[['ID']].copy()
    submission_df['재발방지대책 및 향후조치계획'] = results
    
    submission_df.to_csv(SUBMISSION_PATH, index=False, encoding='utf-8-sig')
    
    print(f"제출 파일이 '{SUBMISSION_PATH}' 경로에 성공적으로 저장되었습니다.")

if __name__ == "__main__":
    main()
