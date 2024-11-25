#!/bin/bash

NAMESPACE="intern"
LABEL_KEY="pod"

# Get all pod names in the namespace
POD_NAMES=$(kubectl get pods -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')

# Loop through each pod name and add a label
for POD_NAME in $POD_NAMES; do
  echo "Labeling pod $POD_NAME with $LABEL_KEY=$POD_NAME"
  kubectl -n $NAMESPACE label pod $POD_NAME $LABEL_KEY=$POD_NAME --overwrite
done
