#!/bin/bash

echo "🧪 Testing Dionysus Backend"
echo "==========================="

# Start the backend in the background
echo "🚀 Starting backend..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for the backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test if the backend is responding
echo "🔍 Testing backend API..."
if curl -s http://localhost:8008/docs > /dev/null; then
    echo "✅ Backend is running successfully!"
    echo "📱 API Documentation: http://localhost:8008/docs"
    echo "🔧 API Base URL: http://localhost:8008"
else
    echo "❌ Backend is not responding on port 8008"
fi

# Stop the backend
echo "🛑 Stopping backend..."
kill $BACKEND_PID 2>/dev/null

echo "✅ Test completed!" 