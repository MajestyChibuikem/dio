#!/bin/bash

echo "🚀 Setting up Dionysus with Docker Desktop"
echo "=========================================="
echo "📝 Note: Using Python 3.12 in Docker containers (your system Python remains unchanged)"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your API keys before continuing"
    echo "   Required API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - WEAVIATE_API_KEY" 
    echo "   - AAI_TOKEN"
    echo "   - GITHUB_PERSONAL_ACCESS_TOKEN"
    echo "   - NOTION_API_KEY"
    echo ""
    echo "   After editing .env, run this script again"
    exit 0
fi

echo "✅ Environment file found"

# Build and start containers
echo "🔨 Building and starting containers..."
docker compose up --build -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if containers are running
echo "🔍 Checking container status..."
docker compose ps

echo ""
echo "🎉 Dionysus is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8008"
echo "🗄️  Database: localhost:5432"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker compose logs -f"
echo "   Stop services: docker compose down"
echo "   Restart services: docker compose restart"
echo ""
echo "⚠️  Note: First startup may take a few minutes as it builds the containers" 