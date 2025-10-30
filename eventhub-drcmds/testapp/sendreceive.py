import os
from azure.eventhub import EventHubProducerClient, EventHubConsumerClient, EventData
from dotenv import load_dotenv
import time

load_dotenv()

CONNECTION_STR = os.getenv("EVENTHUB_CONNECTION_STRING")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")
CONSUMER_GROUP = os.getenv("EVENTHUB_CONSUMER_GROUP", "$Default")



print("CONNECTION_STR:", repr(CONNECTION_STR))
print("EVENTHUB_NAME:", EVENTHUB_NAME)
print("CONSUMER_GROUP:", CONSUMER_GROUP)

# ---- SEND MESSAGES ----
def send_messages():
    print("📤 Connecting producer...")
    producer = EventHubProducerClient.from_connection_string(CONNECTION_STR)
    with producer:
        batch = producer.create_batch()
        for i in range(5):
            batch.add(EventData(f"Message {i+1}"))
        producer.send_batch(batch)
        print("✅ Sent 5 messages!")

# ---- RECEIVE MESSAGES ----
def on_event(partition_context, event):
    print(f"🎯 Received event from partition {partition_context.partition_id}: {event.body_as_str()}")
    partition_context.update_checkpoint(event)

def receive_messages():
    print("👂 Connecting consumer...")
    consumer = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group=CONSUMER_GROUP
    )
    with consumer:
        consumer.receive(
            on_event=on_event,
            starting_position="-1"  # from beginning
        )


if __name__ == "__main__":
    send_messages()
    print("⏳ Waiting 2 seconds before receiving messages...")
    time.sleep(2)
    receive_messages()


