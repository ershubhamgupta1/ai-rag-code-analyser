# TODO: agent tools
from retrieval.semantic_search import (
    SemanticSearch
)

from retrieval.graph_search import (
    GraphSearch
)


class AgentTools:

    def __init__(self):

        self.semantic_search = (
            SemanticSearch()
        )

        self.graph_search = (
            GraphSearch()
        )

    # -------------------------
    # Search Code
    # -------------------------

    def search_code(
        self,
        query,
        limit=10
    ):

        return (
            self.semantic_search
            .search(
                query=query,
                limit=limit
            )
        )

    # -------------------------
    # Get File
    # -------------------------

    def get_file(
        self,
        file_name
    ):

        results = (
            self.semantic_search
            .search(
                query=file_name,
                limit=20
            )
        )

        for item in results:

            if (
                item.get(
                    "name"
                ) == file_name
                or
                item.get(
                    "path",
                    ""
                ).endswith(
                    file_name
                )
            ):
                return item

        return None

    # -------------------------
    # Get Component
    # -------------------------

    def get_component(
        self,
        component_name
    ):

        results = (
            self.semantic_search
            .search(
                query=component_name,
                limit=20
            )
        )

        return [
            r
            for r in results
            if r.get("type")
            == "component"
        ]

    # -------------------------
    # Get Function
    # -------------------------

    def get_function(
        self,
        function_name
    ):

        results = (
            self.semantic_search
            .search(
                query=function_name,
                limit=20
            )
        )

        return [
            r
            for r in results
            if r.get("type")
            == "function"
        ]

    # -------------------------
    # Get API
    # -------------------------

    def get_api(
        self,
        endpoint
    ):

        results = (
            self.semantic_search
            .search(
                query=endpoint,
                limit=20
            )
        )

        return [
            r
            for r in results
            if r.get("type")
            == "api"
        ]

    # -------------------------
    # Trace Execution Flow
    # -------------------------

    def trace_execution_flow(
        self,
        node_name
    ):

        return (
            self.graph_search
            .get_execution_flow(
                node_name
            )
        )

    # -------------------------
    # Get Dependencies
    # -------------------------

    def get_dependencies(
        self,
        node_name
    ):

        return (
            self.graph_search
            .get_dependencies(
                node_name
            )
        )

    # -------------------------
    # Find Callers
    # -------------------------

    def get_callers(
        self,
        function_name
    ):

        return (
            self.graph_search
            .get_callers(
                function_name
            )
        )

    # -------------------------
    # Trace API Flow
    # -------------------------

    def trace_api_flow(
        self,
        endpoint
    ):

        return (
            self.graph_search
            .trace_api_flow(
                endpoint
            )
        )