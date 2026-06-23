from typing import List


class ContextBuilder:

    def build_context(
        self,
        question: str,
        semantic_results: List,
        graph_results: List = None
    ) -> str:

        context_parts = []

        context_parts.append(
            f"""
            User Question:
            {question}
            """
        )

        context_parts.append(
            self._build_semantic_context(
                semantic_results
            )
        )

        if graph_results:
            context_parts.append(
                self._build_graph_context(
                    graph_results
                )
            )
        return "\n".join(context_parts)

    def _build_semantic_context(
        self,
        results
    ):

        sections = []

        sections.append(
            "\n=== RELEVANT CODE ===\n"
        )

        for result in results:

            payload = result

            sections.append(
                f"""
                Type:
                {payload.get('type')}

                Name:
                {payload.get('name')}

                Path:
                {payload.get('path')}

                Code:
                {payload.get('content')[:3000]}
                """
                            )

        return "\n".join(sections)

    def _build_graph_context(
        self,
        graph_results
    ):

        sections = []

        sections.append(
            "\n=== EXECUTION FLOW ===\n"
        )

        for path in graph_results:

            flow = []

            for node in path:

                flow.append(
                    f"{node.get('name')} ({node.get('type')})"
                )

            sections.append(
                " -> ".join(flow)
            )

        return "\n".join(sections)