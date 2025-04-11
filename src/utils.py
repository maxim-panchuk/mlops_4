from sklearn.metrics import classification_report
import configparser
import pandas as pd
from typing import Dict, Any
from src.logger import Logger

class ModelUtils:
    def __init__(self):
        """
        Initialize ModelUtils with configuration
        """
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.output_file = self.config['train']['output_file']

    def evaluate(self, model, X_test, y_test):
        """
        Output classification_report.
        
        Arg:
            model: Trained model
            X_test: Test features
            y_test: Test target
        """
        pred = model.predict(X_test)
        print(classification_report(y_test, pred))


class ModelEvaluator:
    def __init__(self, logger: Logger):
        """
        Initialize ModelEvaluator
        
        Args:
            logger: Logger instance
        """
        self.logger = logger

    def evaluate(self, model: Any, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
        """
        Evaluate model performance and generate classification report
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dictionary containing evaluation metrics
        """
        self.logger.info("Evaluating model performance")
        predictions = model.predict(X_test)
        report = classification_report(y_test, predictions, output_dict=True)
        
        self.logger.info(f"Model evaluation completed. Accuracy: {report['accuracy']:.4f}")
        return report