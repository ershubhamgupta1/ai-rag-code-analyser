from qdrant_client import QdrantClient

from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)
_storage = None

class QdrantStorage:

    def __init__(
        self,
        host="localhost",
        port=6333,
        collection_name="react_codebase"
    ):

        self.collection_name = (
            collection_name
        )

        self.client = QdrantClient(
            host=host,
            port=port
        )

        self._create_collection()

    def _create_collection(self):

        collections = (
            self.client.get_collections()
        )

        exists = any(
            c.name == self.collection_name
            for c in collections.collections
        )

        if exists:
            return

        self.client.create_collection(
            collection_name=
                self.collection_name,

            vectors_config=
                VectorParams(
                    size=384,
                    distance=
                    Distance.COSINE
                )
        )

        print(
            f"Collection created: "
            f"{self.collection_name}"
        )

    def insert_documents(
        self,
        points
    ):

        self.client.upsert(
            collection_name=
                self.collection_name,

            points=points
        )
    def search(self, query_vector,limit=10):

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True
        )

        return response.points

    def delete_collection(
        self
    ):

        self.client.delete_collection(
            collection_name=
                self.collection_name
        )

    def collection_info(
        self
    ):

        return self.client.get_collection(
            self.collection_name
        )


def get_qdrant_client():
    global _storage

    if _storage is None:
        _storage = QdrantStorage()

    return _storage