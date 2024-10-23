import sys
sys.path.append("./libs")

from libs import agent, comms, events, logs
import threading as th

import openai as oai
import json

class LLMAgent(agent.SingleResponsibilityAgent):
    
    def __init__(self, name:str, config:dict, client=None):
        super().__init__(name, config)
        self.client = client
        self.host = config.get("host")
        logs.log_info(f"Agent {name} created")

    def send_message(self, message:str, tag:str):
        comms.dispatch_message(self.host, self.out_queue, message, tag, dispatch_fn=comms.dispatch_rabbitmq_queue)
        comms.dispatch_message(self.host, self.events, message, tag, dispatch_fn=comms.dispatch_rabbitmq_topic)


    
    def start(self):

        def ev(ch, method, properties, body):
            logs.log_info(f"LLM Received {body} {properties.headers[comms.K_TAG]}")
        
            #send prompt to LLM
            if properties.headers[comms.K_TAG] == events.PROMPT_EVENT.get_name():
                logs.log_info("Prompting LLM")
                response = chat(json.loads(body), client=self.client)
                logs.log_info(f"LLM Response: {response}")
                self.send_message(response, "LLM_RESPONSE")
                
                    
        logs.log_info(f"Starting agent... {self.name}")
        comms.consumer_rabbitmq_queue(self.host, self.in_queue, ev)

def chat(messages: list[dict], client:oai.Client=None)-> str:
    return json.dumps(agent.serialize_completion(client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )))
        


if __name__=="__main__":

    openai = oai.OpenAI()
    llmAgent = LLMAgent("llm_agent", {"host":"localhost"}, client=openai)
    llmAgent.start()

    input("Press Enter to exit...")
