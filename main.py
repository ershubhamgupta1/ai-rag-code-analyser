import sys

from ingestion.loader import ProjectLoader
from ingestion.parser import ReactParser
from ingestion.chunker import CodeChunker
from ingestion.indexer import CodeIndexer

from agent.code_agent import CodeAgent


def index_repository(project_path):

    print("\nLoading project...")

    loader = ProjectLoader(project_path)

    files = loader.load_project()

    print(f"Loaded {len(files)} files")

    parser = ReactParser()

    chunker = CodeChunker()

    all_chunks = []

    for file in files:

        parsed_file = parser.parse_file(file)
        if parsed_file["file_name"] == "AuthService.ts":
            print("\n========== AUTH SERVICE PARSED ==========")
            print(parsed_file)

        chunks = chunker.create_chunks(
            parsed_file
        )

        all_chunks.extend(chunks)

    print(
        f"Generated {len(all_chunks)} chunks"
    )

    print(
        "\nIndexing into Qdrant..."
    )

    indexer = CodeIndexer()

    indexer.index_documents(
        all_chunks
    )

    print(
        "\nRepository indexed successfully."
    )


def start_chat():

    print(
        "\nCode Intelligence Agent"
    )

    print(
        "Type 'exit' to quit\n"
    )

    agent = CodeAgent()

    while True:

        question = input(
            "\nAsk: "
        )

        if question.lower() == "exit":
            break

        try:

            answer = agent.answer(
                question
            )

            print("\n")
            print(answer)

        except Exception as ex:

            print(
                f"\nError: {ex}"
            )


def main():

    if len(sys.argv) < 2:

        print(
            """
Usage:

Index Repository:
python main.py index <project_path>

Chat:
python main.py chat
"""
        )

        return

    command = sys.argv[1]

    if command == "index":

        if len(sys.argv) < 3:

            print(
                "Provide project path"
            )

            return

        project_path = sys.argv[2]

        index_repository(
            project_path
        )

    elif command == "chat":

        start_chat()

    else:

        print(
            f"Unknown command: {command}"
        )


if __name__ == "__main__":
    main()