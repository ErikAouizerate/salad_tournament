#!/bin/bash

# Download latest code
git pull
# Build new app image
docker compose build web
# Deploy new version
docker rollout web