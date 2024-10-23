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

#Base Agent for Langchain
# Tools, LLMs, Prompts

