import pandas as pd
import chromadb
import uuid


import os

class Portfolio:
    def __init__(self, file_path=None):
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), "resource", "my_portfolio.csv")
        self.file_path = file_path
        self.data = pd.read_csv(file_path, encoding="latin1")  # or "ISO-8859-1"
        vectorstore_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vectorstore')
        self.chroma_client = chromadb.PersistentClient(vectorstore_path)
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        if not skills or len(skills) == 0:
            return []
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
