import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
    BitsAndBytesConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
)
from src.config import (
    HF_TOKEN,
    INITIAL_MODEL_ID,
    REFINE_MODEL_ID,
    INITIAL_MODEL_MAX_NEW_TOKENS,
    REFINE_MODEL_MAX_NEW_TOKENS,
    MODEL_TEMPERATURE,
    MODEL_TOP_P,
)

def load_initial_model_and_tokenizer() -> tuple[pipeline, PreTrainedTokenizer]:
    """
    초안 답변 생성을 위한 Llama 모델과 토크나이저를 로드하여 파이프라인을 생성합니다.

    Returns:
        tuple: 생성된 text-generation 파이프라인과 토크나이저.
    """
    print(f"초안 생성 모델({INITIAL_MODEL_ID})을 로드합니다...")
    tokenizer = AutoTokenizer.from_pretrained(INITIAL_MODEL_ID, token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(
        INITIAL_MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto",
        token=HF_TOKEN
    )
    
    pipe = pipeline(
        model=model,
        tokenizer=tokenizer,
        task="text-generation",
        do_sample=True,
        temperature=MODEL_TEMPERATURE,
        return_full_text=False,
        max_new_tokens=INITIAL_MODEL_MAX_NEW_TOKENS,
    )
    print("초안 생성 모델 로드가 완료되었습니다.")
    return pipe, tokenizer

def load_refine_model_and_tokenizer() -> tuple[pipeline, PreTrainedTokenizer]:
    """
    답변 정제를 위한 Qwen 모델과 토크나이저를 로드하여 파이프라인을 생성합니다.
    (8비트 양자화 적용)

    Returns:
        tuple: 생성된 text-generation 파이프라인과 토크나이저.
    """
    print(f"정제 모델({REFINE_MODEL_ID})을 로드합니다 (8-bit 양자화 적용)...")
    
    bnb_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_threshold=6.0,
        llm_int8_skip_modules=["lm_head"],
    )
    
    tokenizer = AutoTokenizer.from_pretrained(REFINE_MODEL_ID, token=HF_TOKEN)
    tokenizer.padding_side = "left"
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        REFINE_MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        token=HF_TOKEN,
    )

    pipe = pipeline(
        model=model,
        tokenizer=tokenizer,
        task="text-generation",
        do_sample=True,
        temperature=MODEL_TEMPERATURE,
        top_p=MODEL_TOP_P,
        return_full_text=False,
        max_new_tokens=REFINE_MODEL_MAX_NEW_TOKENS,
    )
    print("정제 모델 로드가 완료되었습니다.")
    return pipe, tokenizer
