#from gigachat import GigaChat
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from gigachat.models import Chat, Messages, MessagesRole
from chromadb.config import Settings
from langchain_gigachat.embeddings.gigachat import GigaChatEmbeddings
from langchain_chroma import Chroma

from langchain.chains import RetrievalQA
from langchain_gigachat.chat_models import GigaChat
from stream_handler import StreamHandler

from langchain.schema import HumanMessage

class GigaRAG:

    def __init__(self):
        with open('gigachatcredentials', 'r', encoding='utf-8') as file:
            line = file.readline()  # Читаем первую строку
            self.credentials = line

        self.chat = GigaChat(
            credentials=self.credentials,
            scope="GIGACHAT_API_PERS",
            model="GigaChat",
            streaming=False,
            verify_ssl_certs=False,
            #callbacks=[StreamHandler()]
        )

        self.embeddings = GigaChatEmbeddings(
            credentials=self.credentials, verify_ssl_certs=False
        )
        self.report = ''
        self.persist_directory = "./chroma_db"  # Директория для сохранения базы данных


    def generate(self, prompt):
        return self.chat([HumanMessage(content=prompt)])

    def load(self, file):
        self.loader = TextLoader(file, encoding="utf-8")
        self.documents = self.loader.load()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        self.documents = self.text_splitter.split_documents(self.documents)
        print(f"Total documents: {len(self.documents)}")

    def create_embeddings(self):
        self.db = Chroma.from_documents(
            self.documents,
            self.embeddings,
            client_settings=Settings(anonymized_telemetry=False),
            persist_directory=self.persist_directory
        )
        #self.db.persist()

    def load_database(self):
        # Загрузка существующей базы данных
        self.db = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,  # Указываем директорию для загрузки
            client_settings=Settings(anonymized_telemetry=False)
        )
        print(f"База данных успешно загружена из директории: {self.persist_directory}")

    def create_qa_chain(self):
        self.qa_chain = RetrievalQA.from_chain_type(self.chat, retriever=self.db.as_retriever())

    def ask_chain(self, query):
        answer = self.qa_chain({"query": query})
        return answer['result']

    def test(self):
        self.load("self-concept.txt")
        self.create_embeddings()
        self.create_qa_chain()
        s = self.ask_chain("Кто ты?")
        print(s)

    def test2(self):
        self.load_database()
        self.create_qa_chain()
        s = self.ask_chain("Кто ты?")
        print(s)

    def test3(self):
        print(self.generate("Напиши последовательность действий робота для пожимания руки в виде простых команд, например: согнуть локоть 90 градусов, согнуть большой палец 0 градусов..."))
