import re
from kiwipiepy import Kiwi

# 띄어쓰기 및 맞춤법 교정을 위한 Kiwi 객체 초기화
# 이 객체는 여러 함수에서 공유하여 사용됩니다.
kiwi = Kiwi()

def clean_text(text: str) -> str:
    """정규식을 사용하여 텍스트에서 불필요한 기호, 번호 등을 제거합니다."""
    text = re.sub(r'\(\d+\)', '', text)  # (1), (2), ...
    text = re.sub(r'\([가-힣]\)', '', text)  # (가), (나), ...
    text = re.sub(r'\bo\b', '', text)  # "o"
    text = re.sub(r'\b\d{1,2}\.\d{1,2}\b', '', text)  # 1.1, 99.99
    text = re.sub(r'\b(?:[1-9]|1[0-9]|20)\.\s', '', text) # 1. , 2. ...
    text = re.sub(r'[\u2460-\u2473]', '', text)  # ①, ②, ...
    return text

def apply_spacing_correction(text: str) -> str:
    """
    Kiwipiepy 라이브러리를 사용하여 텍스트의 띄어쓰기와 맞춤법을 교정합니다.

    Args:
        text (str): 교정할 텍스트.

    Returns:
        str: 교정이 완료된 텍스트.
    """
    try:
        # 형태소 분석
        analyzed = kiwi.analyze(text)
        if not analyzed or not analyzed[0]:
            return text

        # 형태소 리스트 추출
        morphs = [(morph.form, morph.tag) for morph in analyzed[0][0]]

        # 형태소를 다시 조합하여 자연스러운 문장 생성
        final_text = kiwi.join(morphs)
        return final_text
    except Exception:
        # 분석 중 오류 발생 시 원본 텍스트 반환
        return text
