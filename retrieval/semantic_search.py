from sentence_transformers import (
    SentenceTransformer
)

from storage.qdrant_client import (
    get_qdrant_client
)


class SemanticSearch:

    def __init__(
        self,
        collection_name="react_codebase"
    ):

        self.collection_name = collection_name

        self.qdrant = (
            get_qdrant_client()
        )

        self.embedding_model = (
            SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        )

    def search(
        self,
        query,
        limit=10
    ):

        query_vector = (
            self.embedding_model
            .encode(query)
            .tolist()
        )

        results = self.qdrant.search(
            query_vector=query_vector,
            limit=limit
        )

        formatted = []

        for result in results:

            formatted.append({
                "score": result.score,
                **result.payload
            })

        return formatted