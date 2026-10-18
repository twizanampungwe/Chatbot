"""
Streamlit User Interface for the Collaborative Transformer Chatbot.
Complies with project interface and traceability standards.
"""

import streamlit as st
import json

# Page configuration
st.set_page_config(
    page_title="Collaborative Book-Grounded Chatbot",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Book-Grounded Chatbot")
st.markdown("Ask technical questions grounded in our group's assigned textbook repository[span_11](start_span)[span_11](end_span)[span_12](start_span)[span_12](end_span).")

# Mock database or loader for demonstration when offline
def mock_retrieve(question: str, top_k: int = 3):
    """Simulates the common retrieval function interface[span_13](start_span)[span_13](end_span)."""
    # Sample mock passage matching the project schema
    mock_passages = [
        {
            "group_id": "G01",
            "subject": "Computer Science",
            "book_id": "G01_BOOK_001",
            "title": "Computer Organization and Design",
            "page": 45,
            "chunk_id": "G01_BOOK_001_P045_C01",
            "text": "Pipelining is an implementation technique where multiple instructions are overlapped in execution.",
            "score": 0.92
        },
        {
            "group_id": "G01",
            "subject": "Computer Science",
            "book_id": "G01_BOOK_005",
            "title": "Operating System Concepts",
            "page": 112,
            "chunk_id": "G01_BOOK_005_P112_C02",
            "text": "A process is a program in execution. It is the unit of work in a modern operating system.",
            "score": 0.88
        }
    ]
    
    # Simple keyword filter for offline testing
    results = [p for p in mock_passages if any(word.lower() in p["text"].lower() for word in question.split())]
    return results[:top_k] if results else mock_passages[:1] # Fallback for demo

def generate_response(question: str):
    """Generates the answer response structure and handles abstention[span_14](start_span)[span_14](end_span)[span_15](start_span)[span_15](end_span)."""
    retrieved_passages = mock_retrieve(question)
    
    # Handle insufficient evidence check
    if not question.strip():
        return {
            "answer": "Please enter a valid question.",
            "sources": [],
            "insufficient_evidence": True
        }
        
    # Construct response matching project specifications
    sources_list = [
        {
            "book_id": p["book_id"],
            "title": p["title"],
            "page": p["page"],
            "chunk_id": p["chunk_id"]
        }
        for p in retrieved_passages
    ]
    
    answer_text = f"Based on the analyzed textbook literature: {retrieved_passages[0]['text']}"
    
    return {
        "answer": answer_text,
        "sources": sources_list,
        "insufficient_evidence": False
    }

# User Input Form
user_query = st.text_input("Enter your question:", placeholder="e.g., What is pipelining?")

if st.button("Submit Question"):
    if user_query:
        with st.spinner("Retrieving evidence and generating answer..."):
            response = generate_response(user_query)
            
            st.markdown("### Answer")
            st.write(response["answer"])
            
            if response["insufficient_evidence"]:
                st.warning("System Notice: Insufficient evidence found in the assigned books.")
            
            st.markdown("### Traceable Sources")
            if response["sources"]:
                for src in response["sources"]:
                    st.info(f"📖 **Book ID:** {src['book_id']} | **Title:** {src['title']} | **Page:** {src['page']} | **Chunk:** {src['chunk_id']}")
            else:
                st.write("No sources cited.")
    else:
                st.error("Please provide a question before submitting.")
