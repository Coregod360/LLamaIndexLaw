import os
import openai
from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from llama_index import VectorStoreIndex, SimpleDirectoryReader


documents = SimpleDirectoryReader('./data').load_data()

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

response = query_engine.query("what does the the law about Time of election say")
print(response)

