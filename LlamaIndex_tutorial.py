from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser

parser = SimpleNodeParser()
documents = SimpleDirectoryReader('./data').load_data()

nodes = parser.get_nodes_from_documents(documents)
print(nodes)