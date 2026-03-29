import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


DATA_PATH = "data"
INDEX_PATH = "faiss_index"


def load_documents():
    documents = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(DATA_PATH, file))
            docs = loader.load()
            documents.extend(docs)

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def build_index():
    print("Loading documents...")
    documents = load_documents()

    print("Splitting documents...")
    chunks = split_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    print("Creating embeddings...")
    embeddings = create_embeddings()

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    print("Saving index...")
    vectorstore.save_local(INDEX_PATH)

    print("Index built successfully!")


if __name__ == "__main__":
    build_index()