from kafka import KafkaConsumer
import json
import os
from src.database.mongodb import MongoDB

class Consumer:
    def __init__(self):
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        if bootstrap_servers is None:
            raise Exception("no KAFKA_BOOTSTRAP_SERVERS sepicified!")
        print(f"KAFKA_BOOTSTRAP_SERVERS: {bootstrap_servers}")

        self.consumer = KafkaConsumer(
            "banknote_predictions",
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )

        self.db = MongoDB()

    def start_listener(self):
        for message in self.consumer:
            print(f'Message received: {message.value}', flush=True)
            record = message.value
            self.db.save_model_result("banknote_predictions", int(record[0]))

if __name__ == "__main__":
    Consumer().start_listener()
