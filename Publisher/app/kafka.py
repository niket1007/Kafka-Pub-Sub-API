import ssl
from aiokafka import AIOKafkaProducer
from decouple import config
import json

class KafkaProducer:
    _instance = None
    producer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def init_connection(self):
        try:
            context = ssl.create_default_context()
            self.producer = AIOKafkaProducer(
                bootstrap_servers=config("kafka_bootstrap_server", cast=str),
                security_protocol="SASL_SSL", # Use SASL_PLAINTEXT for SASL auth without SSL
                sasl_mechanism="PLAIN",
                ssl_context=context,
                sasl_plain_username=config("kafka_api_key", cast=str),
                sasl_plain_password=config("kafka_api_secret", cast=str),
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8'),
                acks=config("kafka_acks", cast=int)
            )

            await self.producer.start()
        except Exception as e:
            print(f"Error starting Kafka producer: {e}")
            if self.producer:
                await self.stop()
    
    async def push_message_with_zero_acks(self, body: dict, key: str):
        result = self.producer.send(
            topic=config("kafka_topic", cast=str),
            value=body,
            key=key
        )
        print(f"Message sent successfully: {result}")
        return result
    
    async def push_message_with_one_acks(self, body: dict, key: str):
        result = await self.producer.send_and_wait(
            topic=config("kafka_topic", cast=str),
            value=body,
            key=key
        )
        print(f"Message sent successfully: {result}")
        return result

    async def stop(self):
        await self.producer.stop()