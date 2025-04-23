from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import json, os
from src.config import Config

class KafkaManager:
    def __init__(self, config_path: str = "config.ini"):
        self.config = Config(config_path)
        self.kafka_config = self.config.get_kafka_config()
        
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", self.kafka_config["bootstrap_servers"])
        
        print(f"KAFKA_BOOTSTRAP_SERVERS: {bootstrap_servers}")
        
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        self._ensure_topic_exists()
    
    def _ensure_topic_exists(self):
        """Проверяет существование топика и создает его при необходимости с указанным числом партиций"""
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=self.kafka_config["bootstrap_servers"]
            )
            
            topics = admin_client.list_topics()
            
            if self.kafka_config["topic"] not in topics:
                print(f"Creating topic {self.kafka_config['topic']} with {self.kafka_config['num_partitions']} partitions")
                topic = NewTopic(
                    name=self.kafka_config["topic"],
                    num_partitions=self.kafka_config["num_partitions"],
                    replication_factor=self.kafka_config["replication_factor"]
                )
                admin_client.create_topics([topic])
                print(f"Topic {self.kafka_config['topic']} created successfully")
            else:
                print(f"Topic {self.kafka_config['topic']} already exists")
                
            admin_client.close()
        except Exception as e:
            print(f"Error creating topic: {str(e)}")

    def send_message(self, topic: str = None, message: dict = None):
        if topic is None:
            topic = self.kafka_config["topic"]
        self.producer.send(topic, message)
        self.producer.flush()
