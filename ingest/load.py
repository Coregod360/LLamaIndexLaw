import os
import sys
from llama_index import Document , ListIndex
from llama_index.node_parser import SimpleNodeParser
from llama_index import VectorStoreIndex
from llama_index import LLMPredictor, VectorStoreIndex, ServiceContext
from langchain import OpenAI
from llama_index import StorageContext, load_index_from_storage


storage_context = StorageContext.from_defaults()
parser = SimpleNodeParser()



def main(filtered, metadata):
    print("load")
    chunkSize = 1024
    textS3Bucket = 'lawlet-uscode'
    vectorS3Bucket = 'lawlet-uscode-vectors'
    localVectorDir = 'vectorstore'
    allChunks = []
    documents = []
    storage_context = StorageContext.from_defaults(persist_dir="localVectorDir")
    index = load_index_from_storage(storage_context)
    for i in range(len(filtered)):
        row = filtered[i]
        firstLine = row.split("\n")[0]
        body = row.split("\n")[1]
        concat = firstLine + body
        localfilename = './sqldump/'+ metadata[0] + "-" + metadata[0] + '.txt'
        S3filename = 's3://'+ textS3Bucket +'/' + metadata[0] + "-" + metadata[0] + '.txt'
        with open(localfilename, 'a') as f:
            f.write(concat)
        os.system('s3cmd put '+ localfilename + ' ' + "s3://"+ textS3Bucket +"/")
        documents.append(
            Document(
                text=concat,
                metadata={
                    'filename': localfilename,
                    'S3filename': S3filename,
                    'title': metadata[2],
                    'number': metadata[0],
                    'name': metadata[1]
                }
            )
        )
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
    nodes = parser.get_nodes_from_documents(documents)
    storage_context.docstore.add_documents(nodes)
    #index = VectorStoreIndex(nodes)
    thisVectorIndex = VectorStoreIndex(nodes, storage_context=storage_context)
    thisListIndex = ListIndex(nodes, storage_context=storage_context)
    thisVectorIndex.storage_context.persist(persist_dir=localVectorDir)
    os.system('s3cmd put '+ localVectorDir + ' ' + "s3://"+ vectorS3Bucket +"/")

if __name__ == '__main__':
    main()