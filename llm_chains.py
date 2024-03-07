from prompt_templates import memory_prompt_template, pdf_chat_prompt
from langchain.chains import LLMChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from utils import load_config
import chromadb

config = load_config()

def load_ollama_model():
    llm = Ollama(model=config["ollama_model"])
    return llm

def create_llm(model_path = config["ctransformers"]["model_path"]["large"], model_type = config["ctransformers"]["model_type"], model_config = config["ctransformers"]["model_config"]):
    llm = CTransformers(model=model_path, model_type=model_type, config=model_config)
    return llm

def create_embeddings(embeddings_path = config["embeddings_path"]):
    return HuggingFaceInstructEmbeddings(model_name=embeddings_path)

def create_chat_memory(chat_history):
    return ConversationBufferWindowMemory(memory_key="history", chat_memory=chat_history, k=3)

def create_prompt_from_template(template):
    return PromptTemplate.from_template(template)

def create_llm_chain(llm, chat_prompt):
    return LLMChain(llm=llm, prompt=chat_prompt)
    
def load_normal_chain():
    return chatChain()

def load_vectordb(embeddings):
    persistent_client = chromadb.PersistentClient(config["chromadb"]["chromadb_path"])

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name=config["chromadb"]["collection_name"],
        embedding_function=embeddings,
    )

    return langchain_chroma

def load_pdf_chat_chain():
    return pdfChatChain2()

def load_retrieval_chain(llm, vector_db):
    return RetrievalQA.from_llm(llm=llm, retriever=vector_db.as_retriever(kwargs={"k": 3}), verbose=True)

class pdfChatChain:

    def __init__(self):
        vector_db = load_vectordb(create_embeddings())
        llm = create_llm()
        #llm = load_ollama_model()
        self.llm_chain = load_retrieval_chain(llm, vector_db)

    def run(self, user_input, chat_history):
        print("Pdf chat chain is running...")
        return self.llm_chain.invoke(input={"query" : user_input, "history" : chat_history} ,stop=["Human:"],verbose=True)["result"]

class chatChain:

    def __init__(self):
        llm = create_llm()
        #llm = load_ollama_model()
        chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain = create_llm_chain(llm, chat_prompt)

    def run(self, user_input, chat_history):
        return self.llm_chain.invoke(input={"human_input" : user_input, "history" : chat_history} ,stop=["Human:"])["text"]
    
class pdfChatChain2:

    def __init__(self):
        self.vector_db = load_vectordb(create_embeddings())
        llm = create_llm()
        self.llm_chain = create_llm_chain(llm, create_prompt_from_template(pdf_chat_prompt))

    def run(self, user_input, chat_history):
        output = self.vector_db.similarity_search(user_input, k=3)
        context = ""
        for item in output:
            context += item.page_content
        print("Pdf chat chain is running...")
        return self.llm_chain.invoke(input={"context" : context, "user_input" : user_input, "chat_history" : chat_history}, stop=["Context:","Question:"])["text"]