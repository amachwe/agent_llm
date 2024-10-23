import sys
sys.path.append("./libs")

from libs import agent, comms, events, logs, openai_request
from llm_agent import LLMAgent
import json
import pymongo
from sentence_transformers import SentenceTransformer
import time 

if __name__ == "__main__":
    client = pymongo.MongoClient()
    collection = client.get_database("open_ai_test").get_collection("conversations")
    conv_id = time.time()
    sentence_trf = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    HOST = "localhost"
    QUEUE = LLMAgent("llm_agent",{}).get_in_queue()
    loops = 0
    convo = []
    def sys_ev_callback(ch, method, properties, body):
        global loops
        global convo
        loops += 1
        if loops > 20:
            print("Conversation Ended")
            print(convo)
            return
        logs.log_info(f"Sys Event Received {body} {properties.headers[comms.K_TAG]}")
        json_body = json.loads(body)
        resp = json_body.get("choices")[0].get("message").get("content")
        convo.append(resp)
        logs.l("conversation",f"{resp}\n", f"{loops}")
        collection.insert_one({"conv_id":conv_id, "response":resp, "loop":loops, "vector":sentence_trf.encode(resp).tolist()})
        print(loops)
        request = openai_request.build_user(resp)
        comms.dispatch_message(HOST, QUEUE, json.dumps(request), events.PROMPT_EVENT.get_name(), dispatch_fn=comms.dispatch_rabbitmq_queue)

    
    comms.consumer_rabbitmq_topic(HOST, events.SYSTEM_EVENT_QUEUE, callback=sys_ev_callback)

    request = openai_request.build_user("Hello, how are you?")
    comms.dispatch_message(HOST, QUEUE, json.dumps(request) , events.PROMPT_EVENT.get_name(), dispatch_fn=comms.dispatch_rabbitmq_queue)

    input("Press Enter to continue...")