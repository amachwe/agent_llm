from gen_ai_web_server import llm_client
import uuid
import sqlite3

import datetime as dt

class History(object):
    """
    The History class is used to store the conversation history and roles of the participants
    """

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
    #SQL Tool
    cur = sqlite3.connect(DB_NAME).cursor()
    try:
        return execute_query(query, cur)
    except Exception as e:
        return f"Error: {e}"

def get_user_response(question):
    #Ask a Question Tool
    return input(f"Provide response to the question: {question}")

def tool_runner(chat_response):
    """
    Select the correct tool based on the input
    """
    lines = chat_response.split("\n")
    
    for _input in reversed(lines):
        
        if "<Q>" in _input and "</Q>" in _input:
            query = _input.split("<Q>")[1].split("</Q>")[0]
            result = get_user_response(query)
            print("\tResponse (Ask A Question Tool): ",result)
            return result
        elif "<SQL>" in _input and "</SQL>" in _input:
            query = _input.split("<SQL>")[1].split("</SQL>")[0]
            result = execute_sql(query)
            result = f"<RESULT>{result}</RESULT>"
            print("\tResponse (SQL Tool):",result)
            return result
        elif "<R>" in _input and "</R>" in _input:
            # Answer the Question Tool
            result = _input.split("<R>")[1].split("</R>")[0]
            print("Are you happy with the answer? ",result)
            check = input("Enter 'y' or 'n': ")
            if check == "y":
                return None
            else:
                resp = input("How can I help you further?")
                return f"User needs further help {resp}"
    
    raise ValueError(f"Correct tool not found in the input.", {str(input)})

def execute_query(query: str, cursor: sqlite3.Cursor)->None:
   """
   Execute the SQL query returned by the LLM given an open cursor and print the results
   """
   results = ""
   for line in query.split(";"):
        if line == "":
            continue
        text = line+";"
        print("Executing: ", text)
        
        try:
          res = cursor.execute(text)
          for row in res.fetchall():
                results += str(row) + "\n"
          return results  
        except sqlite3.OperationalError as oe:
          print("Error: ", oe,"\nStatement: ", text)
          


if __name__ == "__main__":

    ## Configuring the connection and headers
    DB_NAME = "db/marketplace.db"

    # Maximum number of loops in interaction
    MAX_LOOPS = 12

    ## Create the database and return a cursor to it
    cur = sqlite3.connect(DB_NAME).cursor()

    ## Create the client for LLM
    client = llm_client.OpenAIClient()

    print("\n\n=========\n")
    question = input("Ask your question: ")

    ddl = """CREATE TABLE users (
    user_id      INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    address      TEXT    NOT NULL,
    joining_date TEXT    NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id          REFERENCES users (user_id) 
                     NOT NULL,
    quantity INTEGER NOT NULL,
    price    REAL    NOT NULL
);
"""

    prompt = f"""
    You are an AI assistant that can take one action at a time to help a user with a question: {question}
    You cannot answer without querying for the data. You are allowed to answer without asking a follow up question.
    You can only select ONE action per response. Do not create a SQL query if you do not have enough information.

    Do not repeat the input provided by the user as part of the response.

    Use tags below to indicate the action you want to take:
    ## Run SQL query within the following tags in one line: <SQL> </SQL>. You cannot execute a query - only generate it.
    ## Ask a follow up question to the user - surround question with tags in one line: <Q> </Q>. 
    ## If you have enough data to give final answer to the user's question use tags in one line: <R> </R>.

    Data schema:
    {ddl}
    """

    h = History()
    
    for l in range(MAX_LOOPS):
        
        h.add(prompt, "user") #add input trigger to LLM
        response = client.send_request([{"role":"user", "content": prompt}])
        text = client.extract_response(response)
        h.add(text, "assistant") #add LLM response to history

        print(f"\n{l} LLM Response: ", text)

        #run the tool
        resp = tool_runner(text)
        if resp == None:
            print("\n=== Done ===\n")
            break

        # mini prompt to trigger the LLM
        prompt = f"""{h.concat_input()} Response of tool: {resp} """
 
        if l == MAX_LOOPS-1:
            print("Max loops reached. Exiting...")

        