ROLE_SYSTEM = "system"
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"

K_ROLE = "role"
K_CONTENT = "content"

def build_system(content:str, message:list=None)->list[dict]:
    c = {K_ROLE:ROLE_SYSTEM, K_CONTENT:content}
    if message:
        return [c] + message
    return [c]
    

def build_user(content:str, message:list=None)->list[dict]:
    c= {K_ROLE:ROLE_USER, K_CONTENT:content}
    if message:
        return [c] + message
    return [c]

def build_assistant(content:str, message:list=None)->list[dict]:
    c= {K_ROLE:ROLE_ASSISTANT, K_CONTENT:content}
    if message:
        return [c] + message
    
    return [c]
    



# [{"role":"system", "content":"Hello, how are you?"}]


