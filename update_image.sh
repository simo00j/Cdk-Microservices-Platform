#!/bin/bash

DEPLOYMENT_NAME=$1
IMAGE=$2
CONFIG_FILE="configs/project_config.json"

# Check if the deployment name exists in any of the deployments
exists=$(jq --arg DEPLOYMENT_NAME "$DEPLOYMENT_NAME" '.projects[].deployments[] | select(.deployment_name==$DEPLOYMENT_NAME)' $CONFIG_FILE)

if [ -n "$exists" ]; then
  # Update the image where deployment_name matches
  jq --arg DEPLOYMENT_NAME "$DEPLOYMENT_NAME" --arg IMAGE "$IMAGE" '(.projects[].deployments[] | select(.deployment_name==$DEPLOYMENT_NAME) | .image) |= $IMAGE' $CONFIG_FILE > temp.json && mv temp.json $CONFIG_FILE
else
  # Add a new deployment with the specified deployment_name and image
  jq --arg DEPLOYMENT_NAME "$DEPLOYMENT_NAME" --arg IMAGE "$IMAGE" '(.projects[].deployments += [{"deployment_name":$DEPLOYMENT_NAME, "image":$IMAGE, "ram":2, "cpu":1, "disk":20, "type":"task"}])' $CONFIG_FILE > temp.json && mv temp.json $CONFIG_FILE
fi
