
# from qdrant_client import models
# from sentence_transformers.SentenceTransformer import SentenceTransformer

from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Batch, Distance, VectorParams

from vectorstore.base import BaseVectorStore
from utils.embeddings import embed_german_text

from utils.embeddings import get_embedding_3_large_simple

from utils.helpers import flatten

from utils.logging import get_logger

logger = get_logger(__name__)

from app.core.config import qdrant_settings












class QdrantDatabaseConnector:
    _instance: QdrantClient | None = None

    def __init__(self) -> None:
        if self._instance is None:
            try:
                if qdrant_settings.USE_QDRANT_CLOUD:
                    self._instance = QdrantClient(
                        url=qdrant_settings.QDRANT_CLOUD_URL,
                        api_key=qdrant_settings.QDRANT_APIKEY,
                    )
                else:
                    self._instance = QdrantClient(
                        host=qdrant_settings.QDRANT_DATABASE_HOST,
                        port=qdrant_settings.QDRANT_DATABASE_PORT,
                    )
            except UnexpectedResponse:
                logger.exception(
                    "Couldn't connect to Qdrant.",
                    host=qdrant_settings.QDRANT_DATABASE_HOST,
                    port=qdrant_settings.QDRANT_DATABASE_PORT,
                    url=qdrant_settings.QDRANT_CLOUD_URL,
                )

                raise

    def get_collection(self, collection_name: str):
        return self._instance.get_collection(collection_name=collection_name)

    def create_non_vector_collection(self, collection_name: str):
        self._instance.create_collection(
            collection_name=collection_name, vectors_config={}
        )

    def create_vector_collection(self, collection_name: str):
        self._instance.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=qdrant_settings.EMBEDDING_SIZE, distance=Distance.COSINE
            ),
        )

    def write_data(self, collection_name: str, points: Batch):
        try:
            self._instance.upsert(collection_name=collection_name, points=points)
        except Exception:
            logger.exception("An error occurred while inserting data.")

            raise

    def search(
        self,
        collection_name: str,
        query_vector: list,
        query_filter: models.Filter | None = None,
        limit: int = 3,
    ) -> list:
        return self._instance.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
        )

    def scroll(self, collection_name: str, limit: int):
        return self._instance.scroll(collection_name=collection_name, limit=limit)

    def close(self):
        if self._instance:
            self._instance.close()

            logger.info("Connected to database has been closed.")



class VectorRetriever(BaseVectorStore):
    """
    Class for retrieving vectors from a Vector store in a RAG system using query expansion and Multitenancy search.
    """

    def __init__(self) -> None:
        self._client = QdrantDatabaseConnector()
        # self._embedder = SentenceTransformer(qdrant_settings.EMBEDDING_MODEL_ID)


    def _search_single_query(
        self, query: str, k: int):
        assert k > 3, "k should be greater than 3"

        # query_vector = self._embedder.encode(query).tolist()
        
        # query_vector = embed_german_text(query)
        
        query_vector = get_embedding_3_large_simple(query)

        vectors = [
            self._client.search(
                collection_name=qdrant_settings.QDRANT_COLLECTION_NAME,
                query_vector=query_vector,
                limit=k // 3,
            )
        ]

        return flatten(vectors)

    def search(self, query: str, k: int) -> list:
        hits = self._search_single_query(query, k)
        logger.info("All documents retrieved successfully.", num_documents=len(hits))

        return hits 

    def set_query(self, query: str):
        self.query = query
        
        