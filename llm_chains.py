from prompt_templates import memory_prompt_template, pdf_chat_prompt
from langchain.chains import LLMChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from operator import itemgetter
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
    return pdfChatChain()

def load_retrieval_chain(llm, vector_db):
    return RetrievalQA.from_llm(llm=llm, retriever=vector_db.as_retriever(search_kwargs={"k": config["chat_config"]["number_of_retrieved_documents"]}), verbose=True)

def create_pdf_chat_runnable(llm, vector_db, prompt):
    runnable = (
        {
        "context": itemgetter("human_input") | vector_db.as_retriever(search_kwargs={"k": config["chat_config"]["number_of_retrieved_documents"]}),
        "human_input": itemgetter("human_input"),
        "history" : itemgetter("history"),
        }
    | prompt | llm.bind(stop=["Human:"]) 
    )
    return runnable

class pdfChatChain:

    def __init__(self):
        vector_db = load_vectordb(create_embeddings())
        llm = create_llm()
        #llm = load_ollama_model()
        prompt = create_prompt_from_template(pdf_chat_prompt)
        self.llm_chain = create_pdf_chat_runnable(llm, vector_db, prompt)

    def run(self, user_input, chat_history):
        print("Pdf chat chain is running...")
        return self.llm_chain.invoke(input={"human_input" : user_input, "history" : chat_history})

class chatChain:

    def __init__(self):
        llm = create_llm()
        #llm = load_ollama_model()
        chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain = create_llm_chain(llm, chat_prompt)

    def run(self, user_input, chat_history):
        return self.llm_chain.invoke(input={"human_input" : user_input, "history" : chat_history} ,stop=["Human:"])["text"]