import requests
import json
import datetime


if __name__ == "__main__":
    TARGET_URL = "http://localhost:5000"
    REQUEST_URL = f"{TARGET_URL}/request"
    VOCAB_URL = f"{TARGET_URL}/vocab"
    headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive",

    }

    prompt_math = "What is 14+5*34?"
    data = {
        "prompt": [{"role":"user", "content":prompt_math}],
        "process_logits": False
    }
    print("Sent", datetime.datetime.now())
    # vocab = requests.get(VOCAB_URL).json()
    # print(vocab)
    response = requests.post(REQUEST_URL, data=json.dumps(data), headers=headers).json()
    print(response.get("response"))#
    # print(response.get("logits"))
    # print(response.get("score"))
    print("Received", datetime.datetime.now())