import spacy
from docx import Document
import os

# Load the industrial-strength model
nlp = spacy.load("en_core_web_sm")

def extract_tags_from_docx(file_path):
    # 1. Read the Word Document
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs if para.text.strip() != ""]
    text = " ".join(full_text)
    
    # 2. Process with spaCy (using pipes for speed)
    # nlp.pipe is more efficient for large text
    processed_doc = nlp(text)
    
    # 3. Extract Tags (Noun Chunks & Entities)
    # We filter out common stop words to keep important phrases
    tags = set()
    
    # Extract noun phrases (e.g., "cloud computing", "strategic planning")
    for chunk in processed_doc.noun_chunks:
        if not chunk.root.is_stop and len(chunk.text) > 2:
            tags.add(chunk.text.lower())
            
    # Extract Named Entities (e.g., "Google", "Python", "ISO 9001")
    for ent in processed_doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "GPE", "NORP"]:
            tags.add(ent.text.lower())
            
    return list(tags)

# 4. Automate for 80+ documents
folder_path = "C:\Zafar\python\/nlp"
all_results = {}

for filename in os.listdir(folder_path):
    if filename.endswith(".docx"):
        file_path = os.path.join(folder_path, filename)
        all_results[filename] = extract_tags_from_docx(file_path)

print(all_results)