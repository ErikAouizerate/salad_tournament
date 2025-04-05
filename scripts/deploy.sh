#!/bin/bash

# Download latest code
git pull
# Build new app image
docker compose build salad_backend_python
# Deploy new version
docker rollout salad_backend_python