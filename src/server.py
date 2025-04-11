import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from src.config import Config
from src.logger import Logger
from src.database.mongodb import MongoDB

class InputData(BaseModel):
    variance: float
    skewness: float
    curtosis: float
    entropy: float

class APIServer:
    def __init__(self, config_path: str = "config.ini"):
        self.config = Config(config_path)
        self.logger = Logger(
            name="banknote_api",
            log_file=self.config.get_logging_config()["log_file"],
            level=self.config.get_logging_config()["level"]
        )
        self.model = self._load_model()
        self.app = self._create_app()
        self.db = MongoDB()

    def _load_model(self):
        model_path = self.config.get_train_config()['model_path']
        self.logger.info(f"Loading model from {model_path}")
        try:
            model = joblib.load(model_path)
            self.logger.info("Model loaded successfully")
            return model
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise

    def _create_app(self):
        app = FastAPI(
            title="Banknote Authentication API",
            description="API for predicting banknote authenticity",
            version="1.0.0"
        )

        @app.post("/predict")
        def predict(data: InputData):
            self.logger.info(f"Received prediction request with features: {data.dict()}")
            try:
                new_data = pd.DataFrame([[
                    data.variance,
                    data.skewness,
                    data.curtosis,
                    data.entropy
                ]])

                prediction = self.model.predict(new_data)
                prediction_proba = self.model.predict_proba(new_data)
                
                result = {
                    "prediction": int(prediction[0]),
                    "probability": float(np.max(prediction_proba[0]))
                }

                self.db.save_model_result('banknote_predictions', int(prediction[0]))
                
                self.logger.info(f"Prediction made: {result}")
                return result
                
            except Exception as e:
                self.logger.error(f"Error during prediction: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/health")
        def health_check():
            self.logger.info("Health check requested")
            return {"status": "healthy"}

        return app

    def run(self, host: str = "0.0.0.0", port: int = 8081):
        self.logger.info("Starting API server")
        uvicorn.run(self.app, host=host, port=port)

if __name__ == "__main__":
    server = APIServer()
    server.run(host="0.0.0.0", port=8081)