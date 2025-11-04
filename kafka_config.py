from kafka import KafkaConsumer
from utils import SETTINGS, send_email
from datetime import datetime
import json
import time


def make_consumer(topic, bootstrap_servers, group_id="mail_service-group"):
    """Create and return a Kafka consumer with exponential backoff on connection failure."""
    backoff = 1
    while True:
        try:
            c = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id=group_id,
            )
            print("Connected to Kafka")
            return c
        except Exception as e:
            print(f"Kafka connection failed: {e}. retrying in {backoff}s")
            time.sleep(backoff)
            backoff = min(backoff * 2, 30)


def consume_messages():
    """Consume messages from a specified Kafka topic."""
    if not SETTINGS.USE_KAFKA:
        print(
            "Kafka integration is disabled. Setting USE_KAFKA to True to enable it and restart the service."
        )
        return

    print("Waiting for the producer to start...")

    consumer = make_consumer(
        topic=SETTINGS.KAFKA_CONSUMER_TOPIC,
        bootstrap_servers=SETTINGS.KAFKA_BOOTSTRAP_SERVERS.split(","),
    )

    print("Consumer is ready and listening for messages...")

    try:
        while True:
            for message in consumer:
                ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                key = message.key.decode("utf-8") if message.key else "None"
                data = message.value.decode("utf-8")

                if key == "email_topic":
                    # Get email details from the message
                    email_data = json.loads(data)
                    receiver_email = email_data.get("receiver_email")
                    email_object = email_data.get("email_object")
                    message_text = email_data.get("message_text")

                    if not all([receiver_email, email_object, message_text]):
                        print(f"[{ts}] Incomplete email data received: {email_data}")
                        print("The correct format is:")
                        print(
                            '{"receiver_email": "email@example.com", "email_object": "Subject", "message_text": "Body"} or {"receiver_email": ["email@example.com"], "email_object": "Subject", "message_text": "Body"}'
                        )
                        print("Skipping this message.")
                        continue

                    print(
                        f"[{ts}] Sending email to {receiver_email} with subject '{email_object}'"
                    )
                    # Send the email
                    send_email(
                        receiver_email=receiver_email,
                        message_text=message_text,
                        email_object=email_object,
                    )

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        time.sleep(3)
