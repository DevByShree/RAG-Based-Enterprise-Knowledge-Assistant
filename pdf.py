import fitz
import os

def extract_all_pdfs(folder_path, output_folder="extracted_texts"):
    
    # Output folder banao
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)
            
            full_text = ""
            
            #  Page by page extract karo
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                
                full_text += f"\n\n--- Page {page_num + 1} ---\n\n"
                full_text += page_text
                
                print(f"  📄 Page {page_num + 1}/{len(doc)} extracted...")
            
            #  Saara text ek file mein save karo
            txt_filename = filename.replace(".pdf", ".txt")
            txt_path = os.path.join(output_folder, txt_filename)
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            print(f"Done & Saved: {txt_filename} ({len(doc)} pages)\n")

# Run karo
extract_all_pdfs(r"C:\Users\shree\OneDrive\Desktop\RAG_pdf\data")
print("All DOna PDFs processed! Check the 'extracted_texts' folder for results.")