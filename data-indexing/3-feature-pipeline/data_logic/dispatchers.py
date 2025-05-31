from datetime import datetime
from utils.logging import get_logger
import uuid

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
    @staticmethod
    def handle_mq_message(message: dict) -> DataModel:
        # Add detailed logging to debug the message structure
        logger.info("Raw message received", extra={"message_keys": list(message.keys()) if isinstance(message, dict) else "not_dict", "message_type": type(message).__name__})
        
        data_type = message.get("data_type")
        logger.info("Received message.", extra={"data_type": data_type})

        if not data_type:
            logger.error("No data_type found in message", extra={"message": message})
            raise ValueError("Missing data_type in message")

        if data_type == "pdf_documents":
            try:
                # Parse generated_questions from string to list if needed
                generated_questions = message.get('generated_questions', '')
                if isinstance(generated_questions, str):
                    # Split by newlines and filter empty lines
                    generated_questions_list = [q.strip() for q in generated_questions.split('\n') if q.strip()]
                else:
                    generated_questions_list = generated_questions if isinstance(generated_questions, list) else []

                # Generate a UUID for the entry_id to comply with Qdrant's point ID requirements
                entry_id = str(uuid.uuid4())

                # Create PdfRawModel instance using the message fields
                pdf_raw_model = PdfRawModel(
                    entry_id=entry_id,  # Use UUID instead of filename
                    type=data_type,
                    source=message.get('source', ''),
                    extracted_text=message.get('extracted_text', ''),
                    num_pages=message.get('num_pages', 1),
                    document_title=message.get('document_title', 'Untitled Document'),
                    generated_questions=generated_questions_list  # Fixed field name
                )
                logger.info("PdfRawModel created successfully", extra={"entry_id": pdf_raw_model.entry_id, "source": message.get('source', '')})
                return pdf_raw_model
            except Exception as e:
                logger.error(f"Error creating PdfRawModel: {e}", extra={"message": message})
                raise ValueError(f"Invalid message format: {e}")
        else:
            logger.error(f"Unsupported data type: {data_type}")
            raise ValueError(f"Unsupported data type: {data_type}")


class CleaningHandlerFactory:
    @staticmethod
    def create_handler(data_type: str) -> CleaningDataHandler:
        return PdfCleaningHandler()
        # if data_type == "pdf_documents":
        # else:
        #     raise ValueError(f"Unsupported data type: {data_type}")


class CleaningDispatcher:
    cleaning_factory = CleaningHandlerFactory()

    @classmethod
    def dispatch_cleaner(cls, data_model: DataModel) -> DataModel:
        data_type = data_model.type
        handler = cls.cleaning_factory.create_handler(data_type)
        clean_model = handler.clean(data_model)



        return clean_model


class ChunkingHandlerFactory:
    @staticmethod
    def create_handler(data_type: str) -> ChunkingDataHandler:
        return PdfChunkingHandler()
        # if data_type == "pdf_documents":
        # else:
        #     raise ValueError(f"Unsupported data type: {data_type}")


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
            }
        )

        return chunk_models


class EmbeddingHandlerFactory:
    @staticmethod
    def create_handler(data_type: str) -> EmbeddingDataHandler:
        return PdfEmbeddingHandler()
        # if data_type == "pdf_documents":
        # else:
        #     raise ValueError(f"Unsupported data type: {data_type}")


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
                "embedding_len": len(embedded_chunk_model.embedded_content),
            }
        )

        return embedded_chunk_model
