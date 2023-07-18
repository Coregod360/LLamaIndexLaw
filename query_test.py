import os
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, SimpleDirectoryReader

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

documents = SimpleDirectoryReader('./data').load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("what is afc ajax?")
print(response)

