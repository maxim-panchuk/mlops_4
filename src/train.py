from sklearn.tree import DecisionTreeClassifier, export_graphviz
import joblib
import logging
from typing import List
import pandas as pd

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        """Initialize ModelTrainer"""
        self.model = None
        logger.info("Initialized ModelTrainer")

    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> DecisionTreeClassifier:
        """
        Train the DecisionTreeClassifier.
        
        Args:
            X_train: Training features
            y_train: Training target
            
        Returns:
            Trained model
        """
        logger.info("Starting model training")
        self.model = DecisionTreeClassifier()
        self.model.fit(X_train, y_train)
        
        # Log model performance on training data
        train_score = self.model.score(X_train, y_train)
        logger.info(f"Model training completed. Training accuracy: {train_score:.4f}")
        
        return self.model

    def export_tree(self, feature_names: List[str], class_names_list: List[str], output_file: str) -> None:
        """
        Save the tree structure to a file.
        
        Args:
            feature_names: List of feature names
            class_names_list: List of class names
            output_file: Path to save the tree structure
        """
        logger.info(f"Exporting decision tree structure to {output_file}")
        try:
            export_graphviz(
                self.model,
                out_file=output_file,
                feature_names=feature_names,
                class_names=class_names_list
            )
            logger.info("Tree structure exported successfully")
        except Exception as e:
            logger.error(f"Error exporting tree structure: {str(e)}")
            raise

    def save_model(self, model_path: str) -> None:
        """
        Save the trained model to disk.
        
        Args:
            model_path: Path to save the model
        """
        logger.info(f"Saving model to {model_path}")
        try:
            joblib.dump(self.model, model_path)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Erro saving model: {str(e)}")
            raise