class AppSettings:

    # Embeddings config
    EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL_MAX_INPUT_LENGTH: int = 256
    EMBEDDING_SIZE: int = 384
    EMBEDDING_MODEL_DEVICE: str = "cpu"


    # QdrantDB config
    QDRANT_DATABASE_PORT: int = 6333
    USE_QDRANT_CLOUD: bool = False # if True, fill in QDRANT_CLOUD_URL and QDRANT_APIKEY
    QDRANT_CLOUD_URL: str | None = None
    QDRANT_APIKEY: str | None = None
    QDRANT_DATABASE_HOST: str = "qdrant" # or localhost if running outside Docker
    # QDRANT_DATABASE_HOST="localhost"

    # RAG config
    TOP_K: int = 5
    KEEP_TOP_K: int = 5
    # EXPAND_N_QUERY: int = 5

    # # MQ config
    # RABBITMQ_DEFAULT_USERNAME: str = "guest"
    # RABBITMQ_DEFAULT_PASSWORD: str = "guest"
    # # RABBITMQ_HOST: str = "mq" # or localhost if running outside Docker
    # # RABBITMQ_PORT: int = 5672
    # RABBITMQ_QUEUE_NAME: str = "default"
    # RABBITMQ_PORT: int = 5673 # running bytewax pipeline from localhost(we should use 5673 port here)
    # RABBITMQ_HOST: str = "localhost"

    # CometML config
    # COMET_API_KEY: str
    # COMET_WORKSPACE: str
    # COMET_PROJECT: str = "llm-twin-course"

    # LLM Model config
    TOKENIZERS_PARALLELISM: str = "false"
    HUGGINGFACE_ACCESS_TOKEN: str | None = None
    MODEL_TYPE: str = "mistralai/Mistral-7B-Instruct-v0.1"

    # QWAK_DEPLOYMENT_MODEL_ID: str = "copywriter_model"
    # QWAK_DEPLOYMENT_MODEL_API: str = (
    #     "https://models.llm-twin.qwak.ai/v1/copywriter_model/default/predict"
    # )


settings = AppSettings()
