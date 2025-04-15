from kafka import KafkaProducer
import json, os

class KafkaManager:
    def __init__(self):
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        if bootstrap_servers is None:
            raise Exception("No bootstrap-servers specified!")
        
        print(f"KAFKA_BOOTSTRAP_SERVERS: {bootstrap_servers}")

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic: str, message: dict):
        self.producer.send(topic, message)
        self.producer.flush()
