from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline

def create_qa_chain(llm_pipeline, retriever):
    """
    주어진 LLM 파이프라인과 Retriever를 사용하여 RetrievalQA 체인을 생성합니다.

    Args:
        llm_pipeline: LangChain에서 사용할 text-generation 파이프라인.
        retriever: 질문에 관련된 문서를 검색하는 retriever 객체.

    Returns:
        RetrievalQA: 생성된 QA 체인.
    """
    prompt_template_str = """
### 지침: 당신은 건설 안전 전문가입니다.
주어진 사고 정보를 바탕으로, 구체적이고 실행 가능한 '재발방지대책 및 향후조치계획'만을 답변으로 작성하세요.

### 요구사항:
- 서론, 배경 설명, 사고 원인 분석 등 부가적인 내용은 절대 포함하지 마세요.
- "다음과 같은 조치를 취할 것을 제안합니다:", "제안합니다:" 와 같은 문구는 사용하지 마세요.
- 답변은 오직 대책과 계획에 대한 내용이어야 합니다.

### 맥락 정보:
{context}

### 질문:
{question}

### 답변 (재발방지대책 및 향후조치계획):
"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template_str,
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=HuggingFacePipeline(pipeline=llm_pipeline),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    
    print("RetrievalQA 체인이 생성되었습니다.")
    return qa_chain
