from azure.eventhub import EventHubProducerClient, EventData

connection_str = "Endpoint=sb://nb-failover.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<Sharedaccesskey>;EntityPath=my-eventhub"
producer = EventHubProducerClient.from_connection_string(conn_str=connection_str)

event_data_batch = producer.create_batch()
event_data_batch.add(EventData("Test message"))
producer.send_batch(event_data_batch)
print("✅ Event sent via alias nb-failover")










