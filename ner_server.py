import gen_ai_web_server.llm_server as llm_server
import json



class NERWrapper(llm_server.Wrapper):
    def __init__(self, model_id, model, config):
        self.model = model
        self.config = config
        self.model_id = model_id
        

        if config.get("device", "cpu") == "cuda":
            self.model.to("cuda")
        
    
    def request(self, prompt, *args, **kwargs):
        threshold = config.get("threshold", 0.5)
        text = prompt[0]["text"]
        labels = prompt[0]["labels"]
        entities = self.model.predict_entities(text, labels, threshold)

        return json.dumps({"response":{"entities":entities}})
    
    def get_vocab(self):
        
        return json.dumps({"info":f"This model does not require a vocab {self.model_id}"})
    
    def info(self):
        """
        Get information about the model being wrapped.
        Returns:
            dict: A dictionary containing the name, configuration, and prompting hint for the wrapped model.
        """
        return {
            "name": self.model_id,
            "config": self.config,
            "prompting_hint":self.config["prompting_hint"]
        }

if __name__ == "__main__":

    from gliner import GLiNER

    MODEL_ID = "gliner-community/gliner_large-v2.5"

    model = GLiNER.from_pretrained(MODEL_ID)
    
    

    

    config = {
        "prompting_hint": """messages = [
    {"text": "Text for NER", "labels": ["Name", "Location", "Organization"]}
]""",
"threshold": 0.5,
    "device": "cuda"
    }

    server = llm_server.LLM_Server(NERWrapper(MODEL_ID, model,  config), port=5001)   

    server.start()
