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
    indexS3Bucket = 'lawlet-uscode-index'
    localVectorDir = 'vectorstore'
    localIndexDir = 'indexstore'
    allChunks = []
    documents = []
    if not os.path.exists('./'+ localVectorDir):
        os.makedirs('./'+ localVectorDir)
    if not os.path.exists('./'+ localIndexDir):
        os.makedirs('./'+ localIndexDir)
    listSqlDump = os.listdir('./sqldump')
    if len(listSqlDump) > 0:
        for file in listSqlDump:
            os.remove('./sqldump/'+ file)
    if os.path.exists('./'+ localVectorDir + '/docstore.json'):
        storage_context = StorageContext.from_defaults(persist_dir="localVectorDir")
        index = load_index_from_storage(storage_context)
    else:
        storage_context = StorageContext.from_defaults()
    for i in range(len(filtered)):
        thisMetadata = metadata[i]
        row = filtered[i]
        firstLine = row.split("\n")[0]
        body = row.split("\n")[1]
        concat = firstLine + body
        sqlDumpDir = './sqldump'
        localfilename = './sqldump/'+ thisMetadata[2] + "-" + thisMetadata[0] + '.txt'
        S3filename = 's3://'+ textS3Bucket +'/' + thisMetadata[2] + "-" + thisMetadata[0] + '.txt'
        with open(localfilename, 'a') as f:
            f.write(concat)
        documents.append(
            Document(
                text=concat,
                metadata={
                    'filename': localfilename,
                    'S3filename': S3filename,
                    'title': thisMetadata[2],
                    'number': thisMetadata[0],
                    'name': thisMetadata[1]
                }
            )
        )
    #llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
    print("adding documents to textS3Bucket")
    command = 's3cmd put '+ sqlDumpDir + '/* ' + "s3://"+ textS3Bucket +"/ --recursive"
    print(command)
    os.system(command)
    print("adding documents to nodes")
    nodes = parser.get_nodes_from_documents(documents)
    print("adding nodes to docstore")
    storage_context.docstore.add_documents(nodes)
    print("adding nodes to vectorstore")
    thisVectorIndex = VectorStoreIndex(nodes, storage_context=storage_context)
    print("adding nodes to listindex")
    thisListIndex = ListIndex(nodes, storage_context=storage_context)
    print("persisting vectorstore")
    thisVectorIndex.storage_context.persist(persist_dir=localVectorDir)
    print("persisting listindex")
    thisListIndex.storage_context.persist(persist_dir=localVectorDir)
    print("adding vectorstore to s3")
    os.system('s3cmd put '+ localVectorDir + ' ' + "s3://"+ vectorS3Bucket +"/ --recursive")
    print("adding listindex to s3")
    os.system('s3cmd put '+ localIndexDir + ' ' + "s3://"+ indexS3Bucket +"/ --recursive")
if __name__ == '__main__':
    main()