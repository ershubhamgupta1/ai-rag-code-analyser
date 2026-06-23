import os

from dotenv import load_dotenv
from openai import OpenAI

from agent.tools import AgentTools
from retrieval.context_builder import ContextBuilder

load_dotenv()


class CodeAgent:

    def __init__(self):

        self.tools = AgentTools()

        self.context_builder = (
            ContextBuilder()
        )

        print(
            "OpenAI Key Loaded:",
            bool(
                os.getenv(
                    "OPENAI_API_KEY"
                )
            )
        )

        self.client = OpenAI(
            api_key=os.getenv(
                "OPENAI_API_KEY"
            )
        )

    def answer(self, question):

        semantic_results = (
            self.tools.search_code(
                question
            )
        )

        graph_results = []

        if semantic_results:
            print("Semantic Results:", semantic_results)
            try:

                entity_name = (
                    semantic_results[0]
                    .get("name")
                )
                print("Entity Name:", entity_name)

                graph_results = (
                    self.tools
                    .trace_execution_flow(
                        entity_name
                    )
                )

            except Exception as ex:

                print(
                    "Graph Error:",
                    ex
                )

        context = (
            self.context_builder
            .build_context(
                question=question,
                semantic_results=semantic_results,
                graph_results=graph_results
            )
        )

        prompt = (
            self._build_prompt(
                question,
                context
            )
        )

        response = (
            self.client.chat.completions.create(
                # model="gpt-4.1",
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
                            You are a senior software architect.
                            Analyze the repository and explain architecture.
                            """
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )
        print("Response:", response)
        return (
            response
            .choices[0]
            .message
            .content
        )

    def _build_prompt(
        self,
        question,
        context
    ):
        print("enter in _build_prompt:", context)

        return f"""
            Question:
            {question}

            Context:
            {context}
            """