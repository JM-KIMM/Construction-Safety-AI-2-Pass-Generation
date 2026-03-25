import pandas as pd
from typing import List, Tuple, Optional
from src.config import TRAIN_CSV_PATH, TEST_CSV_PATH

def load_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    훈련 데이터와 테스트 데이터를 CSV 파일에서 로드합니다.

    Returns:
        Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]: 훈련 데이터프레임과 테스트 데이터프레임.
                                                              파일을 찾지 못하면 None을 반환합니다.
    """
    try:
        print(f"'{TRAIN_CSV_PATH}'와 '{TEST_CSV_PATH}'에서 데이터를 로드합니다.")
        train_df = pd.read_csv(TRAIN_CSV_PATH, encoding='utf-8-sig')
        test_df = pd.read_csv(TEST_CSV_PATH, encoding='utf-8-sig')
        return train_df, test_df
    except FileNotFoundError as e:
        print(f"오류: {e}. 'data' 폴더에 train.csv와 test.csv 파일이 있는지 확인하세요.")
        return None, None

def _preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """데이터프레임의 컬럼을 분할합니다."""
    df['공사종류(대분류)'] = df['공사종류'].str.split(' / ').str[0]
    df['공사종류(중분류)'] = df['공사종류'].str.split(' / ').str[1]
    df['공종(대분류)'] = df['공종'].str.split(' > ').str[0]
    df['공종(중분류)'] = df['공종'].str.split(' > ').str[1]
    df['사고객체(대분류)'] = df['사고객체'].str.split(' > ').str[0]
    df['사고객체(중분류)'] = df['사고객체'].str.split(' > ').str[1]
    df['사고원인'] = df['사고원인'].fillna('사고 원인 정보 없음')
    return df

def get_prepared_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """데이터를 로드하고 전처리를 수행합니다."""
    train_df, test_df = load_data()
    if train_df is None or test_df is None:
        return None, None

    print("데이터 전처리를 시작합니다...")
    train_df = _preprocess_dataframe(train_df)
    test_df = _preprocess_dataframe(test_df)
    print("데이터 전처리가 완료되었습니다.")
    
    return train_df, test_df

def create_training_documents(train_df: pd.DataFrame) -> List[str]:
    """
    훈련 데이터프레임으로부터 RAG 검색을 위한 문서 리스트를 생성합니다.
    
    Args:
        train_df (pd.DataFrame): 전처리된 훈련 데이터프레임.

    Returns:
        List[str]: "질문: ... 답변: ..." 형식의 문서 리스트.
    """
    def create_doc(row):
        question = (
            f"공사종류 대분류 '{row['공사종류(대분류)']}', 중분류 '{row['공사종류(중분류)']}' 공사 중 "
            f"공종 대분류 '{row['공종(대분류)']}', 중분류 '{row['공종(중분류)']}' 작업에서 "
            f"사고객체 '{row['사고객체(대분류)']}'(중분류: '{row['사고객체(중분류)']}')와 관련된 사고가 발생했습니다. "
            f"작업 프로세스는 '{row['작업프로세스']}'이며, 사고 원인은 '{row['사고원인']}'입니다. "
            f"재발방지대책 및 향후 조치계획은?"
        )
        answer = row["재발방지대책 및 향후조치계획"]
        return f"질문: {question}
답변: {answer}"

    print("훈련 데이터를 RAG 문서 형식으로 변환합니다...")
    return train_df.apply(create_doc, axis=1).tolist()

def create_test_questions(test_df: pd.DataFrame) -> List[str]:
    """
    테스트 데이터프레임으로부터 모델에 입력할 질문 리스트를 생성합니다.

    Args:
        test_df (pd.DataFrame): 전처리된 테스트 데이터프레임.

    Returns:
        List[str]: 질문 리스트.
    """
    def create_q(row):
        return (
            f"공사종류 대분류 '{row['공사종류(대분류)']}', 중분류 '{row['공사종류(중분류)']}' 공사 중 "
            f"공종 대분류 '{row['공종(대분류)']}', 중분류 '{row['공종(중분류)']}' 작업에서 "
            f"사고객체 '{row['사고객체(대분류)']}'(중분류: '{row['사고객체(중분류)']}')와 관련된 사고가 발생했습니다. "
            f"작업 프로세스는 '{row['작업프로세스']}'이며, 사고 원인은 '{row['사고원인']}'입니다. "
            f"재발방지대책 및 향후조치계획은?"
        )
    print("테스트 데이터의 질문을 생성합니다...")
    return test_df.apply(create_q, axis=1).tolist()
