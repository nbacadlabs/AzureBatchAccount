# Connect to Azure
Connect-AzAccount -UseDeviceAuthentication
Add-Type -Path "$env:USERPROFILE\.nuget\packages\azure.messaging.eventhubs\<version>\lib\netstandard2.0\Azure.Messaging.EventHubs.dll"
Add-Type -Path "$env:USERPROFILE\.nuget\packages\azure.messaging.eventhubs\<version>\lib\netstandard2.0\Azure.Messaging.EventHubs.Producer.dll"

# Variables
$resourceGroup = "eventhub-replication-rg"
$namespace = "nb-primary-ehnamespace"
$eventHub = "nb-primary-hub"
$consumerGroup = '$Default'

# Get authorization key
$key = (Get-AzEventHubKey -ResourceGroupName $resourceGroup -Namespace $namespace -EventHubName $eventHub -Name "testkey").PrimaryKey
$connectionString = "Endpoint=sb://$namespace.servicebus.windows.net/;SharedAccessKeyName=testkey;SharedAccessKey=$key;EntityPath=$eventHub"

# Send a test event
Send-AzEventHubMessage -EventHubName $eventHub -ResourceGroupName $resourceGroup -Namespace $namespace -Message "Hello from PowerShell"

Write-Host "Test event sent successfully!"


