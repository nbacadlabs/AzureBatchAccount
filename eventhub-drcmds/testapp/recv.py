import os
from azure.eventhub import EventHubConsumerClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STR = os.getenv("EVENTHUB_CONNECTION_STRING")
CONSUMER_GROUP = os.getenv("EVENTHUB_CONSUMER_GROUP", "$Default")

def on_event(partition_context, event):
    print(f"🎯 Partition {partition_context.partition_id}: {event.body_as_str()}")
    partition_context.update_checkpoint(event)

def receive_batch():
    consumer = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group=CONSUMER_GROUP
    )

    # Avoid EventProcessor by manually handling all partitions
    with consumer:
        partition_ids = consumer.get_partition_ids()
        for pid in partition_ids:
            print(f"👂 Listening to partition {pid}")
            consumer.receive(
                on_event=on_event,
                partition_id=pid,
                starting_position="-1"  # from beginning
            )

if __name__ == "__main__":
    receive_batch()


