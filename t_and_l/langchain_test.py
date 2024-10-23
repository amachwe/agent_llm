from langchain_core.prompts import PromptTemplate
from langchain.chains import  LLMChain
from langchain_community.llms import GPT4All, HuggingFaceHub
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter, TokenTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from sentence_transformers.util import dot_score
import numpy as np

ORCA="C:\\Users\\azaha\\AppData\\Local\\nomic.ai\\GPT4All\\orca-2-13b.Q4_0.gguf"
CODELLAMA = "C:\\Users\\azaha\\AppData\\Local\\nomic.ai\\GPT4All\\codellama-7b-python.Q4_0.gguf"
CODELLAMA13B = "C:\\Users\\azaha\\AppData\\Local\\nomic.ai\\GPT4All\\codellama-13b-python.Q4_0.gguf"
url = "http://localhost:3030/test"

url_template = """
Context:
The url and method for getting user info: http://localhost:3030/user GET
The url and method for creating new user: http://localhost:3030/user POST

User query: {query}

Task: Return url and method as json with keys: URL and METHOD

"""
#Task: Return url and method as json with keys: URL and METHOD


question_template = """ Answer the question: {query} """

def setup_llm_prompt_chain(prompt_template):

	prompt_instance = PromptTemplate(template=prompt_template, input_variables=['query'])
	gpt4all = GPT4All(model=ORCA)

	chain = LLMChain(prompt=prompt_instance, llm=gpt4all)

	return chain

#chain = setup_llm_prompt_chain(question_template)

#print(chain.invoke("What is 2+2?"))


chain = setup_llm_prompt_chain(url_template)

print(chain.invoke("I want to register as a new user"))



chain = setup_llm_prompt_chain(url_template)

print(chain.invoke("I want to get details of a user"))

