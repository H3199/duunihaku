#!/bin/bash
set -e

# Run jobs initially
# /app/backend/runner.sh

# Start cron in background
service cron start

uvicorn api.main:app --reload --port 8000
