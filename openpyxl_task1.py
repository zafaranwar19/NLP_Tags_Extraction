import os
import spacy
import pandas as pd
from docx import Document
from openpyxl import Workbook

import my_chromadb as mydb
import my_dashboard as myds

# Load the large model for better accuracy
nlp = spacy.load("en_core_web_trf")

def get_tags(file_path):
    doc_docx = Document(file_path)
    # Extract text from paragraphs (limited to first 50000 chars if memory is an issue)
    text = " ".join([p.text for p in doc_docx.paragraphs])
    
    # Process text
    doc = nlp(text)
    
    # Extract unique noun phrases and entities as tags
    tags = {chunk.text.strip().lower() for chunk in doc.noun_chunks if not chunk.root.is_stop}
    return [text,list(tags)]

def export_to_excel(folder_path, output_file):
    # Initialize an empty list for our data rows
    data_rows = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            print(f"Processing: {filename}...")
            file_path = os.path.join(folder_path, filename)
            
            try:
                info = get_tags(file_path)
                tags = info[1]
                full_text = info[0]
                mydb.save_to_vector_db(filename, tags, full_text)

                # Row structure: [Filename, Tag1, Tag2, Tag3, ...]
                data_rows.append([filename] + tags)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Create a DataFrame
    # Column names will be 'Document Name', 'Tag 1', 'Tag 2', etc.
    # df = pd.DataFrame(data_rows)
    # print(df)
    
    # Export to Excel
    # df.to_excel(os.path.join(folder_path, output_file), index=False, header=False)
    # print(f"Successfully saved tags to {output_file}")

    return data_rows

# Usage
data_rows = export_to_excel("c:\Zafar\python\/nlp\/NLP_Tags_Extraction/MyDocs", "Organization_Capabilities.xlsx")

