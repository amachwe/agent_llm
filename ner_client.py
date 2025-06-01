import requests
import json


if __name__ == "__main__":
    TARGET_URL = "http://localhost:5000"
    REQUEST_URL = f"{TARGET_URL}/request"
    VOCAB_URL = f"{TARGET_URL}/vocab"
    headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive",

    }

 
    data = {
        "prompt": [{"text":"Paris is the capital of France, and the home of the NATO", "labels":["Location", "organization", "Name"]}],
        
    }
    print("Sent")
    vocab = requests.get(VOCAB_URL).json()
    print(vocab)
    response = requests.post(REQUEST_URL, data=json.dumps(data), headers=headers).json()
    print(response.get("response"))
