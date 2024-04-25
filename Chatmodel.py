from langchain_community.llms import HuggingFacePipeline
import os
import pickle
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain.utilities import WikipediaAPIWrapper
from langchain.docstore.document import Document



os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.1",model_kwargs={
    "temperature":0.5,"max_length":128
})


def qa_retrieval(question):

    ## Fetch data or context from wikipedia
    wikipedia = WikipediaAPIWrapper()
    doc = wikipedia.run(question).split('Summary: ')[1]

    ## Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(separators = ["\n\n","\n"," "],chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_text(doc)

    # Create document
    docs = [Document(page_content=t) for t in texts]
    
#    Embedding
    embeddings = HuggingFaceHubEmbeddings()

    # Store embeddings in vector
    vectorindex_openai = FAISS.from_documents(docs,embeddings)
    file_path = "vector_index.pkl"
    with open(file_path,'wb') as f:
        pickle.dump(vectorindex_openai,f)
        
    if os.path.exists(file_path):
        with open(file_path,'rb') as f:
            vectorIndex = pickle.load(f)

    # Chain for Retrieval
    chain = RetrievalQA.from_llm(llm=llm, retriever=vectorIndex.as_retriever())

    input_data = {"query": question}
    result = chain.invoke(input_data, return_only_outputs=True)
    return result['result']