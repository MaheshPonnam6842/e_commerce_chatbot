
import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


faq_path = Path(__file__).parent / "resources" / "faq_data.csv"
chroma_client = chromadb.Client()
collection_name = "faqs"
ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
groq_client= Groq()

def ingest_faq_data(path):
    if collection_name not in [c.name for c in chroma_client.list_collections()]:
        collection = chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=ef
        )
        df = pd.read_csv(path)
        docs = df["question"].tolist()
        metadata = [{"answer": ans} for ans in df["answer"].tolist()]
        ids = [f"ids_{i}" for i in range(len(docs))]

        collection.add(documents=docs,
                       metadatas=metadata,
                       ids=ids)
        print(f"FAQ data successfully ingested into client collection {collection_name}")
    else:
        print(f"Collection {collection_name} already exists")


def get_relevant_qa(query):
    collection = chroma_client.get_collection(name=collection_name)
    result = collection.query(query_texts=[query], n_results=2)

    return result

def faq_chain(query):
    result= get_relevant_qa(query)

    context= ' '.join([r.get('answer') for r in result['metadatas'][0]])

    answer= generate_answer(query,context)

    return answer

def generate_answer(query,context):

    prompt= f'''Given the question and context below, Generate answers based context only.
    If you don't know answer inside the context then say "i don't know". 
    Don't make things up.

    Question: {query}

    Context: {context}'''

    completion = groq_client.chat.completions.create(
        model= os.environ['Groq_model'],
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    ingest_faq_data(faq_path)
    query = "What is your policy on defective products"
    #result = get_relevant_qa(query)
    answer= faq_chain(query)
    print(answer)