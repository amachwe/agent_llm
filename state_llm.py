import gen_ai_web_server.llm_server as llm_server
import gen_ai_web_server.llm_client as llm_client

client_phi = llm_client.Client()
client_gem = llm_client.GeminiClient()
client_oai = llm_client.OpenAIClient()

if __name__ == "__main__":
    creator = client_gem
    judge_client = client_oai


    state = ""
    

    user_input = ""

    while user_input!="exit":
        user_input = input()
        state += user_input + "\n"
        prompt = f"{state}\n"
        response = creator.send_request([{"role": "user", "content": prompt + "\nUser Input: "+user_input}])
        state += "\nModel Response: "+creator.extract_response(response) + "\n"
        print(creator.extract_response(response))
        
    
    
print(state)