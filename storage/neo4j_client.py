from neo4j import GraphDatabase
import os


class Neo4jStorage:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            os.getenv(
                "NEO4J_URI",
                "bolt://localhost:7687"
            ),
            auth=(
                os.getenv(
                    "NEO4J_USERNAME",
                    "neo4j"
                ),
                os.getenv(
                    "NEO4J_PASSWORD",
                    "password"
                )
            )
        )

    def close(self):
        self.driver.close()

    def run_query(
        self,
        query,
        params=None
    ):

        with self.driver.session() as session:

            result = session.run(
                query,
                params or {}
            )

            return list(result)


_driver = None


def get_neo4j_driver():

    global _driver

    if _driver is None:

        storage = Neo4jStorage()

        _driver = storage.driver

    return _driver