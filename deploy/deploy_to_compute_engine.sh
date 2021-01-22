#!/bin/bash

gcloud compute instances create-with-container cartoonize-vm \
  --container-image=docker.io/jamesfallon/cartoonize:latest \
  --zone=us-central1-a \
  --machine-type=f1-micro \
  --boot-disk-size=10GB \
  --tags http-server

gcloud compute firewall-rules create allow-http \
 --allow tcp:5000 --target-tags http-server