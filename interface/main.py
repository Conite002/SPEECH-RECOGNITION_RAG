import sys
import os

# Add parent directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU for TensorFlow

import streamlit as st
from app.downloader import scrape_google_scholar, download_pdf
from app.pdf_processor import extract_text_from_pdf
from app.chunking import chunk_text
from app.vector_store import init_vector_store, add_to_vector_store
from app.retriever import query_vector_store, build_context, remove_duplicate_chunks, extract_unique_sources
from app.utils import sanitize_filename, log, build_custom_prompt_with_sources, generate_response_with_retry

# Initialize vector store
vector_store = init_vector_store("./data/chroma_db")

# Session state to store history
if "query_history" not in st.session_state:
    st.session_state.query_history = []


def start_interface():
    """Streamlit interface for the RAG system."""
    st.title("RAG System for Automatic Speech Recognition")

    # Sidebar: Query History Management
    with st.sidebar:
        st.header("Query History")
        if st.session_state.query_history:
            for idx, query_entry in enumerate(st.session_state.query_history):
                with st.expander(f"Query {idx + 1}: {query_entry['query']}"):
                    st.write(f"**Response:** {query_entry['response']}")
                    if st.button(f"Edit Query {idx + 1}", key=f"edit_{idx}"):
                        st.session_state.query = query_entry['query']
                    if st.button(f"Delete Query {idx + 1}", key=f"delete_{idx}"):
                        del st.session_state.query_history[idx]
                        st.experimental_rerun()  # Refresh sidebar to update history
        else:
            st.write("No queries in history.")

    # Fixed Bottom Search Bar
    st.markdown(
        """
        <style>
        .search-bar {
            position: fixed;
            bottom: 15px;
            left: 15px;
            width: calc(100% - 150px);
        }
        .search-button {
            position: fixed;
            bottom: 15px;
            right: 75px;
            height: 40px;
            width: 40px;
            background-color: #2c6dff;
            border: none;
            border-radius: 50%;
            font-size: 18px;
            color: white;
        }
        .upload-button {
            position: fixed;
            bottom: 15px;
            right: 15px;
            height: 40px;
            width: 40px;
            background-color: #ff5722;
            border: none;
            border-radius: 50%;
            font-size: 18px;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Query Section
    query = st.text_input(
        label="",
        placeholder="Type your query...",
        key="query_input",
        label_visibility="hidden",
        help="Enter your search query here",
    )

    # Search Button
    search_button = st.button("🔍", key="search_button", help="Submit query")
    # Upload PDF Button
    uploaded_file = st.file_uploader("📄", type=["pdf"], label_visibility="hidden", key="upload_bottom")

    if uploaded_file:
        try:
            st.info("Uploading and processing PDF...")
            log(f"Processing uploaded PDF: {uploaded_file.name}")
            pdf_path = f"./data/pdfs/{sanitize_filename(uploaded_file.name)}"
            os.makedirs("./data/pdfs", exist_ok=True)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            content = extract_text_from_pdf(pdf_path)
            chunks = chunk_text(content)
            add_to_vector_store(vector_store, uploaded_file.name, chunks, {"source": "uploaded_pdf"})
            log(f"Added {uploaded_file.name} to the database")
            st.success(f"{uploaded_file.name} has been added to the database.")
        except Exception as e:
            log(f"Error processing uploaded PDF: {e}")
            st.error(f"Failed to process the uploaded file: {e}")

    if search_button and query:
        st.info(f"Processing query: {query}")
        try:
            relevant_chunks = query_vector_store(query, vector_store)
            filtered_chunks = remove_duplicate_chunks(relevant_chunks)
            sources = extract_unique_sources(filtered_chunks)
            context = build_context(filtered_chunks)

            # Build custom prompt and generate response
            st.info("Generating a response from the model...")
            custom_prompt = build_custom_prompt_with_sources(query, context, sources)
            # response = generate_response_with_retry(custom_prompt)
            response = generate_response_with_retry(query)

            # Save query and response to history
            st.session_state.query_history.append({"query": query, "response": response})

            # Display results
            # st.write("**Context:**")
            # st.write(context if context else "No context available.")
            st.write("**Sources:**")
            if sources:
                for source in sources:
                    st.markdown(f"- [Read Article]({source})")
            else:
                st.write("No sources available.")
            # st.write("\n".join(sources) if sources else "No sources available.")
            st.write("**Generated Response:**")
            st.write(response if response else "No response generated.")

        except Exception as e:
            log(f"Error during query processing: {e}")
            st.error(f"Failed to process query: {e}")


if __name__ == "__main__":
    start_interface()
