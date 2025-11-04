import datetime
import aio_pika
import asyncio
from utils import SETTINGS, send_email


async def connect_to_rabbitmq(rabbitmq_url: str = SETTINGS.RABBITMQ_URL) -> tuple:
    try:
        print("Connecting to RabbitMQ...")
        connection = await aio_pika.connect_robust(rabbitmq_url, timeout=5)

        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            SETTINGS.RABBITMQ_EXCHANGE, aio_pika.ExchangeType.TOPIC
        )
        queue = await channel.declare_queue(SETTINGS.RABBITMQ_QUEUE, durable=True)

        await queue.bind(exchange, routing_key=SETTINGS.RABBITMQ_ROUTING_KEY)

        print("Connected to RabbitMQ")
        return connection, exchange, queue
    except Exception as e:
        import traceback

        print(f"Error connecting to RabbitMQ: {e}")
        traceback.print_exc()
        return None, None, None


async def consume_rabbitmq_messages_():
    connection, exchange, queue = await connect_to_rabbitmq()
    if not connection:
        print("Failed to connect to RabbitMQ. Exiting consumer.")
        return

    async with connection:
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        payload = message.body.decode()
                        print(f"Received message from RabbitMQ: {payload}")
                        # Assuming payload is a JSON string with required fields
                        import json

                        data = json.loads(payload)
                        receiver_email = data.get("receiver_email")
                        message_text = data.get("message_text")
                        email_object = data.get("email_object")

                        if not all([receiver_email, message_text, email_object]):
                            print(
                                f"[{datetime.datetime.now()}] Incomplete email data received: {data}"
                            )
                            print("The correct format is:")
                            print(
                                '{"receiver_email": "email@example.com", "email_object": "Subject", "message_text": "Body"} or {"receiver_email": ["email@example.com"], "email_object": "Subject", "message_text": "Body"}'
                            )
                            print("Skipping this message.")
                            continue

                        send_email(receiver_email, message_text, email_object)
                    except Exception as e:
                        print(f"Error processing message: {e}")
                    finally:
                        await asyncio.sleep(3)  # Prevent tight loop


def consume_rabbitmq_messages():
    if not SETTINGS.USE_RABBITMQ:
        print(
            "RabbitMQ integration is disabled. Setting USE_RABBITMQ to True to enable it and restart the service."
        )
        return
    print("Starting RabbitMQ consumer...")
    asyncio.run(consume_rabbitmq_messages_())
