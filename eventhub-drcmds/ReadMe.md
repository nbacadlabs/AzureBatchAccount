## This document highlight some troubleshooting commands and well as steps to perform DR in an environment.

## 1. Testing Geo-DR Failover

<pre><code>
az eventhubs georecovery-alias failover \
     --resource-group eventhub-replication-rg \
     --namespace-name nb-secondary-ehnamespace \
     --alias nb-failover
</code></pre>

>[!NOTE] After this, the alias will point to the secondary namespace
> The client should automatically continue working - no code or connection string changes required.


## 2. Confirma that alias is active and mapped correctly

<pre><code>
az eventhubs georecovery-alias show \
  --resource-group eventhub-replication-rg \
  --namespace-name nb-primary-ehnamespace \
  --alias nb-failover
</code></pre>

>[!INFO] If you see `"role": "Secondary"`, that means **the alias currently points to the secondary** — in that case, try running
> the command below

<pre><code>
az eventhubs georecovery-alias show \
  --resource-group eventhub-replication-rg \
  --namespace-name nb-secondary-ehnamespace \
  --alias nb-failover
</code></pre>

#### List authorization rules:

<pre><code>
az eventhubs eventhub authorization-rule list \
  --resource-group eventhub-replication-rg \
  --namespace-name nb-primary-ehnamespace \
  --eventhub-name nb-primary-hub
</code></pre>

>[!NOTE] Ensure that **both** have an authorization rule named `testkey`.
> If not, manually create it on both namespaces **with identical rights** (Listen / Send / Manage).

#### To regenerate an alias use the command below.

<pre><Code>
az eventhubs eventhub authorization-rule keys list \
  --resource-group eventhub-replication-rg \
  --namespace-name nb-primary-ehnamespace \
  --eventhub-name nb-primary-hub \
  --name testkey
</code></pre>

>[!INFO] It is recommendated to use the alias primary string [**`aliasPrimaryConnectionString`**]

#### Test DNS functionality

```nslookup nb-failover.servicebus.windows.net```

#### Connection test with alias

<pre><code>
az eventhubs eventhub show \
  --resource-group eventhub-replication-rg \
  --namespace-name nb-failover \
  --name nb-primary-hub
</code></pre>

#### Show alias
<pre><code>
az eventhubs georecovery-alias show \
  --resource-group eventhub-replication-rg \
  --namespace-name nb-primary-ehnamespace \
  --alias nb-failover
</code></pre>

>[!INFO] That will confirm whether the alias and rule are set up correctly.

#### Creating Authorization rule

<pre><code>
az eventhubs eventhub authorization-rule create \
  --resource-group eventhub-replication-rg \
  --namespace-name nb-secondary-ehnamespace \
  --eventhub-name nb-primary-hub \
  --name testkey \
  --rights Listen Send
</code></pre>

#### Some useful commands

1. ```nslookup nb-failover.servicebus.windows.net``     ---> Chekc what IP the alias resolves to.

2. ```nslookup nb-primary-ehnamespace.privatelink.servicebus.windows.net```