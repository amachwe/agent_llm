import abc
import events
import typing as t
import json

class SingleResponsibilityAgent(abc.ABC):

    def __init__(self, name:str, config:dict):
        self.name = name
        self.in_queue = events.EVENT_QUEUE_PREFIX+"_"+self.name+"_in"
        self.out_queue = events.EVENT_QUEUE_PREFIX+"_"+self.name+"_out"
        self.events = events.SYSTEM_EVENT_QUEUE
                

    def get_in_queue(self):
        return self.in_queue
    
    def get_out_queue(self):
        return self.out_queue
    
    def get_event_queue(self):
        return self.events
    

def serialize_completion(completion):
    return {
        "id": completion.id,
        "choices": [
            {
                "finish_reason": choice.finish_reason,
                "index": choice.index,
                "message": {
                    "content": choice.message.content,
                    "role": choice.message.role,
                    "function_call": {
                        "arguments": json.loads(
                            choice.message.function_call.arguments) if choice.message.function_call and choice.message.function_call.arguments else None,
                        "name": choice.message.function_call.name
                    } if choice.message and choice.message.function_call else None
                } if choice.message else None
            } for choice in completion.choices
        ],
        "created": completion.created,
        "model": completion.model,
        "object": completion.object,
        "system_fingerprint": completion.system_fingerprint,
        "usage": {
            "completion_tokens": completion.usage.completion_tokens,
            "prompt_tokens": completion.usage.prompt_tokens,
            "total_tokens": completion.usage.total_tokens
        }
    }







