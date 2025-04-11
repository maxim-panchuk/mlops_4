from src.preprocess import Preprocessor
from src.train import ModelTrainer
from src.utils import ModelEvaluator
from src.config import Config
from src.logger import Logger
from typing import Dict, Any

class Pipeline:
    def __init__(self, config_path: str = "config.ini"):
        """
        Initialize the pipeline with configuration
        
        Args:
            config_path: Path to the configuration file
        """
        self.config = Config(config_path)
        self.logger = Logger(
            name="banknote_pipeline",
            log_file=self.config.get_logging_config()["log_file"],
            level=self.config.get_logging_config()["level"]
        )
        
        # Initialize components
        self.preprocessor = None
        self.trainer = None
        self.evaluator = None
        
    def run(self) -> Dict[str, Any]:
        """
        Run the complete pipeline
        
        Returns:
            Dictionary containing pipeline results
        """
        self.logger.info("Starting banknote classification pipeline")
        
        # 1. Load and preprocess data
        self._preprocess_data()
        
        # 2. Train model
        model = self._train_model()
        
        # 3. Export tree structure
        self._export_tree()
        
        # 4. Evaluate model
        evaluation_results = self._evaluate_model(model)
        
        # 5. Save model
        self._save_model()
        
        self.logger.info("Pipeline completed successfully")
        return evaluation_results
        
    def _preprocess_data(self) -> None:
        """Load and preprocess the data"""
        self.logger.info("Loading and preprocessing data")
        
        preprocess_config = self.config.get_preprocess_config()
        self.preprocessor = Preprocessor(preprocess_config["data_path"])
        
        # Load data
        data = self.preprocessor.load_data()
        self.logger.info(f"Loaded {len(data)} samples")
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = self.preprocessor.split_data(
            data,
            test_size=preprocess_config["test_size"],
            random_state=preprocess_config["random_state"]
        )
        self.logger.info(f"Split data into train ({len(self.X_train)} samples) and test ({len(self.X_test)} samples) sets")
        
    def _train_model(self):
        """Train the model"""
        self.logger.info("Starting model training")
        self.trainer = ModelTrainer()
        model = self.trainer.train(self.X_train, self.y_train)
        self.logger.info("Model training completed")
        return model
        
    def _export_tree(self) -> None:
        """Export the decision tree structure"""
        self.logger.info("Exporting decision tree structure")
        train_config = self.config.get_train_config()
        
        class_names_list = [str(cls) for cls in self.y_train.unique().tolist()]
        self.trainer.export_tree(
            feature_names=['variance', 'skewness', 'curtosis', 'entropy'],
            class_names_list=class_names_list,
            output_file=train_config["output_file"]
        )
        self.logger.info(f"Tree structure exported to {train_config['output_file']}")
        
    def _evaluate_model(self, model) -> Dict[str, Any]:
        """Evaluate the model"""
        self.logger.info("Evaluating model performance")
        self.evaluator = ModelEvaluator(self.logger)
        evaluation_results = self.evaluator.evaluate(model, self.X_test, self.y_test)
        return evaluation_results
        
    def _save_model(self) -> None:
        """Save the trained model"""
        train_config = self.config.get_train_config()
        self.logger.info(f"Saving model to {train_config['model_path']}")
        self.trainer.save_model(train_config["model_path"]) 