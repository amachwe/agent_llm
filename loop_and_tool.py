from gen_ai_web_server import llm_client
import uuid

import datetime as dt

class History(object):

    def __init__(self, history=[], roles=set()):
        self.history = history
        self.roles = roles

    def add(self, input, role):
        timestamp = dt.datetime.now()
        self.roles.add(role)
        self.history.append({"role": role, "content": input, "timestamp": timestamp.isoformat(), "id": str(uuid.uuid4())})

    def get_roles(self) -> set:
        return self.roles
    
    def filter(self, role:str) -> object:
        history = [x for x in self.history if x["role"] == role]
        return History(history=history, roles={role})
    
    def get_latest(self) -> dict:
        return self.history[-1]
    
    def get_all(self) -> list:
        return self.history
    
    def get_last_n(self, n:int) -> list:
        return self.history[-n:]
    
    def concat_input(self, n:int = 0) -> str:
        
        return "\n\n".join([f"{str(i)}: {x['content']}" for i, x in enumerate(self.history[-n:])])
    
    def get_all_timestamps(self, n:int = 0)-> str:
        return "\n\n".join([f"{str(i)}: {x['timestamp']}" for i, x in enumerate(self.history[-n:])])
        
    def clear(self):
        self.history = []
        self.roles = set()


def execute_sql(query):
    if "created_at" in query or "date" in query:
        return "Error"
    return "1000"

def get_user_response(question):
    return input(f"Provide response to the question: {question}")

def tool(_input,history):
    #Execute SQL
    
    if "<Q>" in _input and "</Q>" in _input:
        query = _input.split("<Q>")[1].split("</Q>")[0]
        result = get_user_response(query)
        print("Response (CLI Tool):",result)
        return result
    elif "<SQL>" in _input and "</SQL>" in _input:
        query = _input.split("<SQL>")[1].split("</SQL>")[0]
        result = execute_sql(query)
        result = f"<RESULT>{result}</RESULT>"
        print("Response (SQL Tool):",result)
        return result
    elif "<R>" in _input and "</R>" in _input:
        result = _input.split("<R>")[1].split("</R>")[0]
        print("Are you happy with the answer? ",result)
        check = input("Enter 'y' or 'n': ")
        if check == "y":
            return None
        else:
            return "Answer in the response is not correct. Please provide the correct answer."
    else:
        raise ValueError(f"Correct tool not found in the input.", {str(input)})




if __name__ == "__main__":

    import os
    import sqlite3
    ## Configuring the connection and headers
    DB_NAME = "db/marketplace"

    MAX_LOOPS = 10


    ## Remove the database if it exists
    if os.path.exists(DB_NAME):
      os.remove(DB_NAME)

    ## Create the database and return a cursor to it
    cur = sqlite3.connect(DB_NAME).cursor()

    client = llm_client.GeminiClient()

    question = "How many users did we have last month?"


    prompt = f"""
    You are an AI assistant that can take one action at a time to help a user with a question: {question}
    You cannot answer without querying for the data. You are allowed to answer without asking a follow up question.
    You can only select ONE action per response. Do not create a SQL query if you do not have enough information.

    Use tags below to indicate the action you want to take:
    ## Run SQL query within the following tags: <SQL> </SQL>. You cannot execute a query - only generate it.
    ## Ask a follow up question to the user - surround question with tags: <Q> </Q>. 
    ## If you have enough data to give final answer to the user's question use tags: <R> </R>.

    Additional information:

    Schema for the SQL data: 
    Table: users
    columns: user_id, name, email, phone_number, address
    Table: orders
    columns: order_id, user_id, product_id, quantity, price
    """

    h = History()
    
    for l in range(MAX_LOOPS):
        
        h.add(prompt, "user")
        response = client.send_request([{"role":"user", "content": prompt}])
        text = client.extract_response(response)
        h.add(text, "assistant")
        print("Response: ", text)

        resp = tool(text,h)
        if resp == None:
            print("Done")
            break

        prompt = f"""{h.concat_input()} Response of tool: {resp} """
 
    if l == MAX_LOOPS-1:
        print("Max loops reached. Exiting...")

        # response = client.send_request([{"role":"user", "content": prompt}])
        # text = client.extract_response(response)
        # h.add(text, "assistant")
        # print("\n\nResponse: ", text)


        # resp = tool(text,h)

        # prompt = f"""{h.concat_input()} Response of tool: {resp} """
        # response = client.send_request([{"role":"user", "content": prompt}])
        # text = response.content #response["response"][1]["content"]
        # h.add(text, "assistant")
        # print("\n\nResponse: ", text)

        # #conversation history
        # #print(h.concat_input())
        # history = h.concat_input()

        # prompt = f""" Compress the history {history} """

        # response = client.send_request([{"role":"user", "content": prompt}])

        # text = response["response"][1]["content"]
        # print("\n\nResponse: ", text)   
