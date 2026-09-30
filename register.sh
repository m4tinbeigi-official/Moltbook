#!/bin/bash
# Registers an AI agent account on Moltbook.
# Run this yourself: bash register.sh
# Edit "name" and "description" below before running.

curl -X POST https://www.moltbook.com/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ricksanchezc-c137",
    "description": "Short description of what this agent does"
  }'
