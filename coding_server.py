import gen_ai_web_server.llm_server as llm_server


if __name__ == "__main__":

    import transformers

    #MODEL_ID = "microsoft/Phi-3.5-mini-instruct"  
    MODEL_ID = "microsoft/Phi-4-mini-instruct"
    #MODEL_ID = "microsoft/phi-4"
    model = transformers.AutoModelForCausalLM.from_pretrained(MODEL_ID, trust_remote_code=True, local_files_only=False)
    tokenizer = transformers.AutoTokenizer.from_pretrained(MODEL_ID)

    

    config = {
        "prompting_hint": """messages = [
    {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
    {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."},
    {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"},
]""",
    "trust_remote_code": True,
    "device": "cuda"
    }

    server = llm_server.LLM_Server(llm_server.LLM_Server_Pipe_Wrapper(MODEL_ID, tokenizer, model,  config))   

    server.start()
