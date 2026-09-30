import streamlit as st
from QAWithPDF.data_ingestion import load_data
from QAWithPDF.embedding import download_gemini_embedding
from QAWithPDF.model_api import load_model

    
def main():
    st.set_page_config("QA with Documents")
    
    doc=st.file_uploader("upload your document")
    
    st.header("QA with Documents(Information Retrieval)")
    
    user_question= st.text_input("Ask your question")
    
    if st.button("submit & process"):
        with st.spinner("Processing..."):
            document=load_data(doc)
            model=load_model()
            query_engine=download_gemini_embedding(model,document)
                
            try:
                response = query_engine.query(user_question)
                st.write(response.response)
            except Exception as e:
                st.error(f"The model is busy or returned an error. Please try again in a moment.\n\n{e}")
                            
                
if __name__=="__main__":
    main()         
            