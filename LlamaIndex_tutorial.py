import os
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index import VectorStoreIndex

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


parser = SimpleNodeParser()

documents = SimpleDirectoryReader('./data').load_data()

nodes = parser.get_nodes_from_documents(documents)
index = VectorStoreIndex.from_documents(nodes)

print(index.storage_context.index_store)
