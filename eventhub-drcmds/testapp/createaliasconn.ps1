$rg = "eventhub-replication-rg"
$ns = "nb-primary-ehnamespace"
$hub = "nb-primary-hub"
$alias = "nb-failover"

# Fetch the RootManageSharedAccessKey
$key = az eventhubs namespace authorization-rule keys list `
    --resource-group $rg `
    --namespace-name $ns `
    --name RootManageSharedAccessKey | ConvertFrom-Json

# Write to .env with the alias endpoint
$envContent = @"
EVENTHUB_CONNECTION_STRING=Endpoint=sb://$alias.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=$($key.primaryKey);EntityPath=$hub
EVENTHUB_NAME=$hub
EVENTHUB_CONSUMER_GROUP=$Default
"@

Set-Content -Path .env -Value $envContent
Write-Host "✅ .env file updated with alias connection string!"
