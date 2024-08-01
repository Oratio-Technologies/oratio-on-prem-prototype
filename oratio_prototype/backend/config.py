import os
from dotenv import load_dotenv, find_dotenv


# Load environment variables
load_dotenv(find_dotenv())


class Settings:
    MONGODB_PWD = os.getenv("MONGODB_PWD")
    MONGO_DATABASE_HOST = f"mongodb+srv://zoldyck:{MONGODB_PWD}@cluster0.kjantw5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    
    # MONGO_DATABASE_HOST: str = "mongodb://localhost:30001,localhost:30002,localhost:30003/?replicaSet=my-replica-set"

    MONGO_DATABASE_NAME: str = "production"
    
    
settings = Settings()




