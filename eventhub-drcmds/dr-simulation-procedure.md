## To Perform a successful DR, we assume the following are set properly:
    1. Primary and Secondary (failover) namespaces exist
    2. The namespaces are paired

### Step One: Verify Geo-DR Pairing

<pre><code>
az eventhubs georecovery-alias show \
  --alias <ALIAS_NAME> \
  --namespace-name <PRIMARY_NAMESPACE> \
  --resource-group <RESOURCE_GROUP>

  example:
  az eventhubs georecovery-alias show \
  --alias nb-failover \
  --namespace-name nb-primary-ehnamespace \
  --resource-group eventhub-replication-rg


  *** expected output ***
    {
  "id": "/subscriptions/568bb264-0562-4033-9ffd-a52a303ba299/resourceGroups/eventhub-replication-rg/providers/Microsoft.EventHub/namespaces/nb-primary-ehnamespace/disasterRecoveryConfigs/nb-failover",
  "location": "canadacentral",
  "name": "nb-failover",
  "partnerNamespace": "/subscriptions/568bb264-0562-4033-9ffd-a52a303ba299/resourceGroups/eventhub-replication-rg/providers/Microsoft.EventHub/namespaces/nb-secondary-ehnamespace",
  "pendingReplicationOperationsCount": 0,
  "provisioningState": "Succeeded",
  "resourceGroup": "eventhub-replication-rg",
  "role": "Primary",
  "type": "Microsoft.EventHub/Namespaces/disasterrecoveryconfigs"      
}

</code></pre>

### Step two: Test Disaster Recovery (Failover to Secondary)
- To simulate DR, you fail over the alias to the secondary namespace

<pre><code>
az eventhubs georecovery-alias fail-over \
    --alias <ALIAS_NAME> \
    --namespace-name <SECONDARY_NAMESPACE> \
    --resource-group <RESOURCE_GROUP>

    example: 
    az eventhubs georecovery-alias fail-over \
    --alias nb-failover \
    --namespace-name nb-secondary-ehnamespace \
    --resource-group eventhub-replication-rg

    *** Expected Output ***
</code></pre>

> **ℹ️** <br />
> This command does the following <br />
> 1. Promotes the secondary namespace to primary namespace <br />
> 2. Your connection strings that use the alias (e.g. nb-failover.servicebus.windows.net) now point to the secondary automatically. <br />
> 3. No app configuration changes are needed — the alias remains the same.

### Step three: Verify After Failover
- Check if namespace is active

<pre><code>
az eventhubs georecovery-alias show \
  --alias nb-failover \
  --namespace-name nb-secondary \
  --resource-group my-rg

  example:
  az eventhubs georecovery-alias show \
  --alias nb-failover \
  --namespace-name nb-secondary-ehnamespace \
  --resource-group eventhub-replication-rg

  ** expected output **
  {
  "id": "/subscriptions/568bb264-0562-4033-9ffd-a52a303ba299/resourceGroups/eventhub-replication-rg/providers/Microsoft.EventHub/namespaces/nb-secondary-ehnamespace/disasterRecoveryConfigs/nb-failover",
  "location": "canadaeast",
  "name": "nb-failover",
  "partnerNamespace": "",
  "provisioningState": "Succeeded",
  "resourceGroup": "eventhub-replication-rg",
  "role": "PrimaryNotReplicating",
  "type": "Microsoft.EventHub/Namespaces/disasterrecoveryconfigs"      
}

</code></pre>

> **ℹ️** <br />
> Look for ```"role": "Primary"``` — if it’s the secondary, your failover succeeded.

- Test the if your app can send and receive messages.

### Step 4: Re-establish Pairing and Switch Back to Primary

> **📝** <br />
> Failover is one-way — after failover, the `old primary` becomes orphaned. <br />
> You will have to switch back to primary by performing the steps listed below.

#### 1. Delete the old alias (optional cleanup)

<pre><code>
az eventhubs georecovery-alias delete \
  --alias nb-failover \
  --namespace-name nb-secondary-ehnamespace \
  --resource-group eventhub-replication-rg
</code></pre>

#### 2. Recreate the pairing in the new primary (which was previously the secondary)

<pre><code>
az eventhubs georecovery-alias set \
  --alias nb-failover \
  --namespace-name nb-secondary-ehnamespace \
  --partner-namespace nb-primary-ehnamespace \
  --resource-group eventhub-replication-rg
</code></pre>

#### 3. Wait for the replication to complete and confirm using the command below

<pre><code>
az eventhubs georecovery-alias show \
  --name nb-failover \
  --namespace-name nb-secondary-ehnamespace \
  --resource-group my-rg
</code></pre>

>**✅**
> Now we are back in a protected state, with the promoted primary as a secondary again.

> **📝** <br />
> It is worth noting that, <br />
> 1. No manual DNS change is needed. The alias endpoint remains the same
> 2. You can't failback directly; you must recreate the pairing
> 3. Ensure both namespaces are in the same Azure region pair (e.g. Canada Central <-> Canada East)
