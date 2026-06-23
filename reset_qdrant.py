from storage.qdrant_client import (
    get_qdrant_client
)

client = get_qdrant_client()

client.delete_collection()