import configparser
from pathlib import Path
from typing import Any, Dict

class Config:
    def __init__(self, config_path: str = "config.ini"):
        self.config = configparser.ConfigParser()
        self.config_path = Path(config_path)
        self._load_config()
        
    def _load_config(self) -> None:
        """Config loading"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"config file {self.config_path} not found")
        self.config.read(self.config_path)
        
    def get_preprocess_config(self) -> Dict[str, Any]:
        """Preprocess config"""
        return {
            "test_size": self.config.getfloat("preprocess", "test_size"),
            "random_state": self.config.getint("preprocess", "random_state"),
            "data_path": self.config.get("preprocess", "data_path")
        }
    
    def get_train_config(self) -> Dict[str, Any]:
        """Train config"""
        return {
            "model_path": self.config.get("train", "model_path"),
            "output_file": self.config.get("train", "output_file")
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Logging config"""
        return {
            "level": self.config.get("logging", "level"),
            "log_file": self.config.get("logging", "log_file")
        }
    
    def get_all_config(self) -> Dict[str, Dict[str, Any]]:
        """All config"""
        return {
            "preprocess": self.get_preprocess_config(),
            "train": self.get_train_config(),
            "logging": self.get_logging_config()
        } 