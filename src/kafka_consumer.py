from kafka import KafkaConsumer
import json
import os
from src.database.mongodb import MongoDB

class Consumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            "banknote_predictions",
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9091"),
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

        self.db = MongoDB()

    def start_listener(self):
        for message in self.consumer:
            record = message.value
            self.db.save_model_result("banknote_predictions", int(record[0]))

if __name__ == "__main__":
    Consumer().start_listener()
