import streamlit as st
import chromadb

def display():
    st.title("Organization Capability Explorer")

    # Connect to the DB you created
    client = chromadb.PersistentClient(path="./my_vector_db")
    collection = client.get_collection(name="org_capabilities")

    # Search Bar
    query = st.text_input("Search for a capability (e.g., 'Artificial Intelligence'):")

    if query:
        results = collection.query(query_texts=[query], n_results=5)
        
        for i in range(len(results['ids'][0])):
            with st.expander(f"Doc: {results['ids'][0][i]}"):
                st.write(f"**Associated Tags:** {results['metadatas'][0][i]['tags']}")
                st.write(f"**Excerpt:** {results['documents'][0][i][:500]}...")

display()