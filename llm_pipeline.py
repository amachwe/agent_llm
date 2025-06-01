import requests
import json
import gen_ai_web_server.llm_client as llm_client
from bs4 import BeautifulSoup

def build_ner(text, labels):
    return {"prompt":[{"text":text, "labels":labels}]}


if __name__ == "__main__":
    LLM_TARGET_URL = "http://localhost:5000"
    LLM_REQUEST_URL = f"{LLM_TARGET_URL}/request"

    NER_TARGET_URL = "http://localhost:5001"
    NER_REQUEST_URL = f"{NER_TARGET_URL}/request"

    headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive",

    }

    MAX_LOOPS = 10

    QUESTION = "What is nuclear fusion?"
    llm = llm_client.Client()

    response = llm.send_request([{"role":"user", "content":QUESTION}])
    text=(response.get("response")[1]["content"])
    print(text)

    labels = []

    prompt_eval = f"""Generate list of entity labels within <l> </l> tag for the following text: {text}. Current list of labels {labels}"""

    

    for i in range(MAX_LOOPS):
        
        response = llm.send_request([{"role":"user", "content":prompt_eval}])
        print(response)
        
    

    

    #response = requests.post(NER_REQUEST_URL, data=json.dumps(ner_data), headers=headers).json()

    #print(response.get("response"))
