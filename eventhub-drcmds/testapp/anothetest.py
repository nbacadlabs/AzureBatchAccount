from azure.eventhub import EventHubConsumerClient

# Use the alias connection string
connection_str = "Endpoint=sb://nb-failover.servicebus.windows.net/;SharedAccessKeyName=testkey;SharedAccessKey=<sharedaccesskey>;EntityPath=nb-primary-hub"

client = EventHubConsumerClient.from_connection_string(
    conn_str=connection_str,
    consumer_group="$Default"
)

print("Partitions:", client.get_partition_ids())




