import hvac
import os
from typing import Dict, Any
from src.logger import Logger

class VaultClient:
    def __init__(self, vault_url: str = "http://localhost:8200", token: str = None):
        """
        Initialize Vault client
        
        Args:
            vault_url: URL of the Vault server
            token: Root token for authentication (optional, will be read from environment if not provided)
        """
        self.logger = Logger(name="vault_client")
        
        # Read token from environment if not provided
        if token is None:
            token = os.getenv('VAULT_TOKEN')
            if token is None:
                raise ValueError("VAULT_TOKEN environment variable is not set")
                
        self.client = hvac.Client(url=vault_url, token=token)
        
        if not self.client.is_authenticated():
            raise Exception("Failed to authenticate with Vault")
            
        self.logger.info("Successfully authenticated with Vault")
            
        self.setup_mongodb_secrets(
            username=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            db_name=os.getenv("DB_NAME")
        )

        self.logger.info('Successfully initialized Vault')
        
    def write_secret(self, path: str, data: Dict[str, Any]) -> None:
        """
        Write secret to Vault
        
        Args:
            path: Path to store the secret
            data: Secret data to store
        """
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data
            )
            self.logger.info(f"Successfully wrote secret to {path}")
        except Exception as e:
            self.logger.error(f"Failed to write secret: {str(e)}")
            raise
            
    def read_secret(self, path: str) -> Dict[str, Any]:
        """
        Read secret from Vault
        
        Args:
            path: Path to the secret
            
        Returns:
            Secret data
        """
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            self.logger.info(f"Successfully read secret from {path}")
            return response['data']['data']
        except Exception as e:
            self.logger.error(f"Failed to read secret: {str(e)}")
            raise
            
    def setup_mongodb_secrets(self, username: str, password: str, db_name: str) -> None:
        """
        Setup MongoDB secrets in Vault
        
        Args:
            username: mongodb username
            password: MongoDB password
            db_name: MongoDB database name
        """
        mongodb_secrets = {
            "username": username,
            "password": password,
            "db_name": db_name,
            "uri": f"mongodb://{username}:{password}@mongodb:27017/{db_name}?authSource=admin"
        }
        
        self.write_secret("mongodb/credentials", mongodb_secrets)
        self.logger.info("Successfully setup MongoDB secrets in Vault") 