#!/bin/bash

echo "🔄 Rebuilding containers with Python 3.12"
echo "========================================"

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose down

# Remove old images to force rebuild
echo "🗑️  Removing old backend image..."
docker rmi dionysus-backend 2>/dev/null || true

# Rebuild and start
echo "🔨 Rebuilding with Python 3.12..."
docker compose up --build -d

echo ""
echo "✅ Containers rebuilt with Python 3.12!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8008"
echo ""
echo "📋 Check logs: docker compose logs -f" 