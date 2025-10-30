import os
from azure.eventhub import EventHubProducerClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STR = os.getenv("EVENTHUB_CONNECTION_STRING")
# EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")

try:
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR
        # eventhub_name=EVENTHUB_NAME
    )
    with producer:
        print("✅ Successfully connected to Event Hub!")
except Exception as e:
    print("❌ Connection failed:", e)
