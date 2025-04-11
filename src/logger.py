import logging
from pathlib import Path
from typing import Optional

class Logger:
    def __init__(
        self,
        name: str,
        log_file: Optional[str] = None,
        level: int = logging.INFO
    ):
        """
        Initializ logger with console and file handlers
        
        Args:
            name: Logger name
            log_file: Path to log file
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if log_file is specified
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)

    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message) 