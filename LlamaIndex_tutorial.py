import os
from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index import VectorStoreIndex
from llama_index import get_response_synthesizer
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor

os.environ['OPENAI_API_KEY'] = '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'

parser = SimpleNodeParser()
response_synthesizer = get_response_synthesizer()

documents = SimpleDirectoryReader('./data').load_data()

nodes = parser.get_nodes_from_documents(documents)
index = VectorStoreIndex.from_documents(nodes)

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=2,
)

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[
        SimilarityPostprocessor(similarity_cutoff=0.7)
    ]

)

response = query_engine.query("what does the word vessel mean?")
print(response)
