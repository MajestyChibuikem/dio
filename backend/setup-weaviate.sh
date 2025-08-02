#!/bin/bash

echo "🚀 Setting up Weaviate locally..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if weaviate-docker-compose.yml exists
if [ ! -f "weaviate-docker-compose.yml" ]; then
    echo "❌ weaviate-docker-compose.yml not found. Please run this from the backend directory."
    exit 1
fi

# Start Weaviate
echo "📦 Starting Weaviate container..."
docker-compose -f weaviate-docker-compose.yml up -d

# Wait for Weaviate to be ready
echo "⏳ Waiting for Weaviate to be ready..."
sleep 10

# Check if Weaviate is responding
if curl -s http://localhost:8080/v1/.well-known/ready > /dev/null; then
    echo "✅ Weaviate is running at http://localhost:8080"
    echo "🌐 You can access the Weaviate console at: http://localhost:8080/v1/console"
else
    echo "⚠️ Weaviate might still be starting up. Please wait a moment and try again."
fi

echo ""
echo "🎯 To stop Weaviate, run: docker-compose -f weaviate-docker-compose.yml down"
echo "🎯 To view logs, run: docker-compose -f weaviate-docker-compose.yml logs -f" 