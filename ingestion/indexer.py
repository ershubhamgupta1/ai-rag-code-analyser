import uuid

from sentence_transformers import (
    SentenceTransformer
)

from qdrant_client.models import (
    PointStruct
)

from storage.qdrant_client import (
    get_qdrant_client
)

from storage.neo4j_client import (
    Neo4jStorage
)


class CodeIndexer:

    def __init__(
        self,
        collection_name="react_codebase"
    ):

        self.collection_name = (
            collection_name
        )

        self.qdrant = (
            get_qdrant_client()
        )

        self.neo4j = (
            Neo4jStorage()
        )

        self.embedding_model = (
            SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        )

    # ==================================
    # QDRANT
    # ==================================

    def index_documents(
        self,
        chunks
    ):

        points = []

        for chunk in chunks:
            print("===========Index Documents==============")
            if chunk["name"] == "loginApi":
                print("\nLOGIN API CHUNK")
                print(chunk["content"])

            if chunk["name"] == "login":
                print("\nLOGIN CHUNK")
                print(chunk)

            text = (
                self.build_embedding_text(
                    chunk
                )
            )

            vector = (
                self.embedding_model
                .encode(text)
                .tolist()
            )

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=chunk
            )

            points.append(point)

        self.qdrant.insert_documents(
            points
        )

        print(
            f"Indexed "
            f"{len(points)} chunks "
            f"to Qdrant"
        )

        self.index_graph(
            chunks
        )

    # ==================================
    # NEO4J
    # ==================================

    def index_graph(
        self,
        chunks
    ):

        print(
            "Building Neo4j graph..."
        )

        for chunk in chunks:
            print("===========Index Graph==============")
            if chunk["name"] == "loginApi":
                print("\nLOGIN API CHUNK")
                print(chunk["content"])

            if chunk["name"] == "login":
                print("\nLOGIN CHUNK")
                print(chunk)

            self.create_node(
                chunk["name"],
                chunk["type"],
                chunk["path"]
            )

            metadata = (
                chunk.get(
                    "metadata",
                    {}
                )
            )

            # -------------------------
            # COMPONENT -> IMPORTS
            # -------------------------

            if chunk["type"] == "component":

                for imp in metadata.get(
                    "imports",
                    []
                ):

                    self.create_node(
                        imp,
                        "import",
                        ""
                    )

                    self.create_relationship(
                        chunk["name"],
                        imp,
                        "IMPORTS"
                    )

            # -------------------------
            # COMPONENT -> FUNCTION
            # Login -> handleSubmit
            # -------------------------

            if chunk["type"] == "function":
                for fn in metadata.get(
                    "function_calls",
                    []
                ):

                    self.create_node(
                        fn,
                        "function",
                        ""
                    )

                    self.create_relationship(
                        chunk["name"],
                        fn,
                        "CALLS"
                    )
                for component in metadata.get(
                    "components",
                    []
                ):

                    self.create_node(
                        component,
                        "component",
                        ""
                    )

                    self.create_relationship(
                        component,
                        chunk["name"],
                        "CALLS"
                    )

                # -------------------------
                # FUNCTION -> SERVICE
                # handleSubmit ->
                # AuthService.login
                # -------------------------

                for service in metadata.get(
                    "service_calls",
                    []
                ):

                    self.create_node(
                        service,
                        "service",
                        ""
                    )

                    self.create_relationship(
                        chunk["name"],
                        service,
                        "CALLS"
                    )

                # -------------------------
                # FUNCTION -> API
                # -------------------------

                for api in metadata.get(
                    "api_calls",
                    []
                ):

                    print(
                        f"CREATING API RELATIONSHIP: "
                        f"{chunk['name']} -> {api}"
                    )    
                    self.create_node(
                        api,
                        "api",
                        ""
                    )

                    self.create_relationship(
                        chunk["name"],
                        api,
                        "USES_API"
                    )

            # -------------------------
            # FILE -> API
            # authApi.ts -> /api/login
            # -------------------------

            if chunk["type"] == "api":

                file_name = (
                    metadata.get(
                        "file"
                    )
                )

                if file_name:

                    self.create_node(
                        file_name,
                        "file",
                        ""
                    )

                    self.create_relationship(
                        file_name,
                        chunk["name"],
                        "USES_API"
                    )

        print(
            "Neo4j graph indexed"
        )

    # ==================================
    # NODE CREATION
    # ==================================

    def create_node(
        self,
        name,
        node_type,
        path=""
    ):

        self.neo4j.run_query(
            """
            MERGE (n:CodeEntity {
                name:$name
            })

            SET
                n.type=$type,
                n.path=$path
            """,
            {
                "name": name,
                "type": node_type,
                "path": path
            }
        )

    # ==================================
    # RELATIONSHIP CREATION
    # ==================================

    def create_relationship(
        self,
        source,
        target,
        relation
    ):

        query = f"""
        MATCH (a:CodeEntity {{
            name:$source
        }})

        MATCH (b:CodeEntity {{
            name:$target
        }})

        MERGE (a)-[:{relation}]->(b)
        """

        self.neo4j.run_query(
            query,
            {
                "source": source,
                "target": target
            }
        )

    # ==================================
    # EMBEDDINGS
    # ==================================

    def build_embedding_text(
        self,
        chunk
    ):

        return f"""
Type:
{chunk.get('type')}

Name:
{chunk.get('name')}

Path:
{chunk.get('path')}

Content:
{chunk.get('content')}
"""