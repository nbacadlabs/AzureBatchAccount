#!/bin/bash

rgName="nborgs$RANDOM"
region="eastus"
az group create --name $rgName --location $region

namespaceName="nexgbitsns$RANDOM"
az eventhubs namespace create --name $namespaceName --resource-group $rgName -l $region

eventhubName="nbevhubname$RANDOM"
az eventhubs eventhub create --name $eventhubName --resource-group $rgName --namespace-name $namespaceName