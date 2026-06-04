# Here we use lang chain to split the text into chunks and save them in a folder called "chunks". Each chunk is saved as a separate text file.
#LangChain LLM ko real-world data aur tools ke saath connect karne ka framework hai.

import os

def create_chunks(input_folder="extracted_texts", output_folder="chunks", chunk_size=500, overlap=50):
    
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            txt_path = os.path.join(input_folder, filename)
            
            # Text file padhlo
            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            #  Words mein todo
            words = text.split()
            chunks = []
            
            for i in range(0, len(words), chunk_size - overlap):
                chunk = " ".join(words[i:i + chunk_size])
                if chunk:
                    chunks.append(chunk)
            
            #  Chunks save karo
            chunk_filename = filename.replace(".txt", "_chunks.txt")
            chunk_path = os.path.join(output_folder, chunk_filename)
            
            with open(chunk_path, "w", encoding="utf-8") as f:
                for i, chunk in enumerate(chunks):
                    f.write(f"\n\n--- Chunk {i + 1} ---\n\n")
                    f.write(chunk)
            
            print(f" {filename} → {len(chunks)} Done")

# Run karo
create_chunks()
print("\nReady all chunks")