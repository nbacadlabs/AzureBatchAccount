from azure.eventhub import EventHubConsumerClient
import os

from dotenv import load_dotenv
load_dotenv()

CONNECTION_STR = os.getenv("EVENTHUB_CONNECTION_STRING")
CONSUMER_GROUP = "$Default"

try:
    client = EventHubConsumerClient.from_connection_string(CONNECTION_STR, consumer_group=CONSUMER_GROUP)
    with client:
        print("✅ Consumer connection successful!")
except Exception as e:
    print("❌ Consumer failed:", e)
