import os
import asyncio
from aiokafka import AIOKafkaConsumer

async def consume_messages():
    # Use port 9093 for host connections (PLAINTEXT_HOST listener)
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093")

    consumer = AIOKafkaConsumer(
        'xppu_data',
        bootstrap_servers=bootstrap_servers,
    )

    await consumer.start()

    print("Consumer started. Listening for messages...")

    try:
        async for message in consumer:
            print(f"Received message: {message.value.decode('utf-8')}")
            print(f"Topic: {message.topic}, Partition: {message.partition}, Offset: {message.offset}")
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())
