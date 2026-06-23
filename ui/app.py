import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from agent.code_agent import CodeAgent
from ingestion.loader import ProjectLoader
from ingestion.parser import ReactParser
from ingestion.chunker import CodeChunker
from ingestion.indexer import CodeIndexer

st.set_page_config(
    page_title="Code Intelligence",
    layout="wide"
)

st.title("🚀 Code Intelligence Agent")

# ----------------------------------
# Sidebar
# ----------------------------------

with st.sidebar:

    st.header("Repository")

    repo_path = st.text_input(
        "Repository Path",
        "./data/repositories/sample-react-app"
    )

    if st.button("Index Repository"):

        try:

            with st.spinner(
                "Loading repository..."
            ):

                loader = ProjectLoader(
                    repo_path
                )

                files = (
                    loader.load_project()
                )

                parser = ReactParser()

                chunker = CodeChunker()

                all_chunks = []

                for file in files:

                    parsed = (
                        parser.parse_file(
                            file
                        )
                    )

                    chunks = (
                        chunker.create_chunks(
                            parsed
                        )
                    )

                    all_chunks.extend(
                        chunks
                    )

                indexer = CodeIndexer()

                indexer.index_documents(
                    all_chunks
                )

            st.success(
                f"Indexed {len(all_chunks)} chunks"
            )

        except Exception as ex:

            st.error(str(ex))

# ----------------------------------
# Chat UI
# ----------------------------------

if "agent" not in st.session_state:

    st.session_state.agent = (
        CodeAgent()
    )

if "messages" not in st.session_state:

    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

question = st.chat_input(
    "Ask about your codebase..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(question)

    with st.chat_message(
        "assistant"
    ):

        try:

            with st.spinner(
                "Analyzing repository..."
            ):

                response = (
                    st.session_state.agent
                    .answer(question)
                )

                st.markdown(response)

        except Exception as ex:

            response = (
                f"Error: {str(ex)}"
            )

            st.error(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )