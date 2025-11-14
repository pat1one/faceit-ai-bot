#!/bin/bash
cd /home/pat/faceit-ai-bot-4
export NODE_ENV=production
export NODE_OPTIONS="--max-old-space-size=512"
export PORT=3000
export HOSTNAME=0.0.0.0
exec npx next start
