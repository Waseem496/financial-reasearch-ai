from dotenv import load_dotenv
import os

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


class DocumentIngestor:
    def __init__(self):
        self.persist_directory = "data/chroma_db"

        self.embedding = HuggingFaceEmbeddings(
                  model_name="all-MiniLM-L6-v2"
                        )

    def ingest(self, file_path: str):
        print(f"📄 Loading document: {file_path}")

        loader = PyPDFLoader(file_path)
        documents = loader.load()

        print("✂️ Splitting into chunks...")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        print(f"📊 Total chunks: {len(chunks)}")

        print("💾 Storing in ChromaDB...")

        db = Chroma.from_documents(
            chunks,
            self.embedding,
            persist_directory=self.persist_directory
        )

        db.persist()

        print("✅ Ingestion complete!")


if __name__ == "__main__":
    ingestor = DocumentIngestor()

    ingestor.ingest("data/annual_reports/infosys.pdf")