import os
from sentence_transformers import SentenceTransformer
import chromadb

def create_embeddings(chunks_folder="chunks"):
    
    # Embedding model load karo
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    #  ChromaDB create 
    client = chromadb.PersistentClient(path="vector_db")  # Save hoga disk pe
    collection = client.get_or_create_collection(name="my_notes") # creating a collection in vector DB 
    
    all_chunks = []
    all_ids = []
    all_metadata = []
    
    chunk_id = 0
    
    for filename in os.listdir(chunks_folder):
        if filename.endswith("_chunks.txt"):
            chunk_path = os.path.join(chunks_folder, filename)
            
            with open(chunk_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            #  Chunks alag karo
            chunks = content.split("--- Chunk")
            chunks = [c.strip() for c in chunks if c.strip()]
            
            for chunk in chunks:
                all_chunks.append(chunk)
                all_ids.append(str(chunk_id))
                all_metadata.append({"source": filename})  # Kahan se aaya track karo
                chunk_id += 1
            
            print(f" {filename} → {len(chunks)} chunks ready")
    
    #  Embeddings banao aur store karo
    print("\n⏳ Embeddings ban rahi hain...")
    embeddings = model.encode(all_chunks).tolist()
    
    collection.add(
        embeddings=embeddings,
        documents=all_chunks,
        ids=all_ids,
        metadatas=all_metadata
    )
    
    print(f"\n Done! {len(all_chunks)} chunks can be store in ChromaDB!")

create_embeddings()