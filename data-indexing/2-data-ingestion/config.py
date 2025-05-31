import os
from dotenv import load_dotenv, find_dotenv


# Load environment variables
load_dotenv(find_dotenv())


class Settings:
    MONGODB_PWD = os.getenv("MONGODB_PWD")
    MONGO_DATABASE_HOST = f"mongodb+srv://zoldyck:zoldyck@cluster0.kjantw5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    # MongoDB configs
    # MONGO_DATABASE_HOST: str = "mongodb://localhost:30001,localhost:30002,localhost:30003/?replicaSet=my-replica-set"

    # MONGO_DATABASE_HOST: str = (
    #     "mongodb://mongo1:30001,mongo2:30002,mongo3:30003/?replicaSet=my-replica-set"
    # )
    MONGO_DATABASE_NAME: str = "production"


    RABBITMQ_HOST: str = "localhost"  # or the Docker host if running remotely
    RABBITMQ_PORT: int = 5673  # Port mapped in Docker Compose
    RABBITMQ_DEFAULT_USERNAME: str = "guest"  # Default username
    RABBITMQ_DEFAULT_PASSWORD: str = "guest"  # Default password
    RABBITMQ_QUEUE_NAME: str = "default"



class AzureSettings:
    AZURE_OPENAI_API_KEY: str = "mcOZ1fI1JChD4P0fyyp84wEb6dJ0iIBWaSfOALNXXWwSfjj5mM7gJQQJ99AKACHYHv6XJ3w3AAAAACOGH5AI"
    AZURE_OPENAI_ENDPOINT: str = (
        "https://alach-m3n4py1o-eastus2.cognitiveservices.azure.com/openai/"
        "deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"
    )
    AZURE_OPENAI_API_VERSION: str = "2024-08-01-preview"
azure_settings = AzureSettings()


settings = Settings()
