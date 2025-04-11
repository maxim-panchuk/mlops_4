from pymongo import MongoClient
from src.vault_client import VaultClient
from src.logger import Logger
import datetime
import os

class MongoDB:
    def __init__(self, vault_client: VaultClient = None):
        """
        Initialize MongoDB connection using secrets from Vault
        
        Args:
            vault_client: VaultClient instance
        """
        self.logger = Logger(name="mongodb")
        
        if vault_client is None:
            vault_client = VaultClient(vault_url=os.getenv("VAULT_ADDR"), token=os.getenv("VAULT_TOKEN"))
            
        try:
            # Get MongoDB credentials from Vault
            secrets = vault_client.read_secret("mongodb/credentials")
            
            # Initialize MongoDB client
            self.client = MongoClient(secrets["uri"])
            self.db = self.client[secrets["db_name"]]
            
            # Test connection
            self.client.admin.command('ping')
            self.logger.info("Successfully connected to MongoDB")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
            
    def save_model_result(self, collection_name: str, prediction: int) -> None:
        """
        Save model prediction result to MongoDB
        
        Args:
            collection_name: Name of the collection
            prediction: Prediction value
        """
        try:
            collection = self.db[collection_name]
            collection.insert_one({
                "prediction": prediction,
                "timestamp": datetime.datetime.now()
            })
            self.logger.info(f"Successfully saved prediction to {collection_name}")
        except Exception as e:
            self.logger.error(f"Failed to save prediction: {str(e)}")
            raise
            
    def close(self) -> None:
        """Close MongoDB connection"""
        try:
            self.client.close()
            self.logger.info("Successfully closed MongoDB connection")
        except Exception as e:
            self.logger.error(f"Failed to close MongoDB connection: {str(e)}")
            raise 