from storage.neo4j_client import (
    get_neo4j_driver
)


class GraphSearch:

    def __init__(self):

        self.driver = (
            get_neo4j_driver()
        )

    def get_execution_flow(
        self,
        node_name
    ):

        query = """
        MATCH path =
        (n {name:$node_name})
        -[:CALLS*1..5]->
        (m)

        RETURN path
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                node_name=node_name
            )

            return self._parse_paths(
                result
            )

    def get_dependencies(
        self,
        node_name
    ):

        query = """
        MATCH (n {name:$node_name})
        -[:IMPORTS|USES]->
        (m)

        RETURN
        n.name AS source,
        type(
            relationships(
                (n)-[]->(m)
            )[0]
        ) AS relation,
        m.name AS target
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                node_name=node_name
            )

            return [
                record.data()
                for record in result
            ]

    def get_callers(
        self,
        function_name
    ):

        query = """
        MATCH
        (caller)-[:CALLS]->
        (callee {name:$function_name})

        RETURN caller.name
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                function_name=function_name
            )

            return [
                row["caller.name"]
                for row in result
            ]

    def trace_api_flow(
        self,
        endpoint
    ):

        query = """
        MATCH path=
        (n)-[:CALLS*1..10]->
        (api:API {
            endpoint:$endpoint
        })

        RETURN path
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                endpoint=endpoint
            )

            return self._parse_paths(
                result
            )

    def _parse_paths(
        self,
        result
    ):

        flows = []

        for record in result:

            path = record["path"]

            nodes = []

            for node in path.nodes:

                nodes.append(
                    {
                        "name":
                            node.get(
                                "name"
                            ),

                        "type":
                            node.get(
                                "type"
                            )
                    }
                )

            flows.append(nodes)

        return flows