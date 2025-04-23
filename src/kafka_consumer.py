from kafka import KafkaConsumer
import json
import os
from src.database.mongodb import MongoDB
from src.config import Config

class Consumer:
    def __init__(self, config_path: str = "config.ini"):
        self.config = Config(config_path)
        self.kafka_config = self.config.get_kafka_config()
        
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", self.kafka_config["bootstrap_servers"])
        
        print(f"KAFKA_BOOTSTRAP_SERVERS: {bootstrap_servers}")
        print(f"Topic: {self.kafka_config['topic']}")

        self.consumer = KafkaConsumer(
            self.kafka_config["topic"],
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

        self.db = MongoDB()

    def start_listener(self):
        print(f"Starting consumer for topic {self.kafka_config['topic']}")
        for message in self.consumer:
            print(f'Message received: {message.value}', flush=True)
            record = message.value
            self.db.save_model_result(self.kafka_config["topic"], int(record['prediction']))

if __name__ == "__main__":
    Consumer().start_listener()
