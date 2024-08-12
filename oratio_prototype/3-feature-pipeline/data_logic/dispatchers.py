from datetime import datetime
from utils.logging import get_logger

from data_logic.chunking_data_handlers import (
    ChunkingDataHandler,
    PdfChunkingHandler,
)
from data_logic.cleaning_data_handlers import (
    CleaningDataHandler,
    PdfCleaningHandler,
)
from data_logic.embedding_data_handlers import (
    EmbeddingDataHandler,
    PdfEmbeddingHandler,
)
from models.base import DataModel
from models.raw import PdfRawModel

import json

logger = get_logger(__name__)

class RawDispatcher:
    # @staticmethod
    # def handle_mq_message(body: bytes) -> DataModel:
    #     try:
    #         # Decode the message from JSON format
    #         message = json.loads(body.decode())
    #     except json.JSONDecodeError as e:
    #         logger.error(f"Invalid JSON format: {e}")
    #         raise ValueError(f"Invalid JSON format: {e}")
    @staticmethod
    def handle_mq_message(message: dict) -> DataModel:
        data_type = message.get("type")
        logger.info("Received message.", extra={"data_type": data_type})

        if data_type == "pdf_documents":
            try:
                # Create PdfRawModel instance using the message fields
                pdf_raw_model = PdfRawModel(
                    entry_id=message.get('entry_id'),
                    type=message.get('type'),
                    source=message.get('source'),
                    extracted_text=message.get('extracted_text'),
                    num_pages=message.get('num_pages')
                )
                return pdf_raw_model
            except KeyError as e:
                logger.error(f"Missing key in message: {e}")
                raise ValueError(f"Invalid message format: missing {e}")
            except ValueError as e:
                logger.error(f"Value error in message: {e}")
                raise ValueError(f"Invalid message format: {e}")
        else:
            logger.error(f"Unsupported data type: {data_type}")
            raise ValueError(f"Unsupported data type: {data_type}")


class CleaningHandlerFactory:
    @staticmethod
    def create_handler(data_type: str) -> CleaningDataHandler:
        if data_type == "pdf_documents":
            return PdfCleaningHandler()
        else:
            raise ValueError(f"Unsupported data type: {data_type}")


class CleaningDispatcher:
    cleaning_factory = CleaningHandlerFactory()

    @classmethod
    def dispatch_cleaner(cls, data_model: DataModel) -> DataModel:
        data_type = data_model.type
        handler = cls.cleaning_factory.create_handler(data_type)
        clean_model = handler.clean(data_model)

        logger.info(
            "Data cleaned successfully.",
            extra={
                "data_type": data_type,
                "cleaned_content_len": len(clean_model.cleaned_extracted_text),
            }
        )

        return clean_model


class ChunkingHandlerFactory:
    @staticmethod
    def create_handler(data_type: str) -> ChunkingDataHandler:
        if data_type == "pdf_documents":
            return PdfChunkingHandler()
        else:
            raise ValueError(f"Unsupported data type: {data_type}")


class ChunkingDispatcher:
    chunking_factory = ChunkingHandlerFactory()

    @classmethod
    def dispatch_chunker(cls, data_model: DataModel) -> list[DataModel]:
        data_type = data_model.type
        handler = cls.chunking_factory.create_handler(data_type)
        chunk_models = handler.chunk(data_model)

        logger.info(
            "Cleaned content chunked successfully.",
            extra={
                "num_chunks": len(chunk_models),
                "data_type": data_type,
            }
        )

        return chunk_models


class EmbeddingHandlerFactory:
    @staticmethod
    def create_handler(data_type: str) -> EmbeddingDataHandler:
        if data_type == "pdf_documents":
            return PdfEmbeddingHandler()
        else:
            raise ValueError(f"Unsupported data type: {data_type}")


class EmbeddingDispatcher:
    embedding_factory = EmbeddingHandlerFactory()

    @classmethod
    def dispatch_embedder(cls, data_model: DataModel) -> DataModel:
        data_type = data_model.type
        handler = cls.embedding_factory.create_handler(data_type)
        embedded_chunk_model = handler.embedd(data_model)

        logger.info(
            "Chunk embedded successfully.",
            extra={
                "data_type": data_type,
                "embedding_len": len(embedded_chunk_model.embedded_content),
            }
        )

        return embedded_chunk_model
