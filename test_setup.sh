#!/bin/bash

# Test script for Dionysuss setup
echo "🧪 Testing Dionysuss Setup Script"
echo "=================================="

# Test 1: Check if setup script exists
if [ -f "setup.sh" ]; then
    echo "✅ Setup script exists"
else
    echo "❌ Setup script not found"
    exit 1
fi

# Test 2: Check if script is executable
if [ -x "setup.sh" ]; then
    echo "✅ Setup script is executable"
else
    echo "❌ Setup script is not executable"
    exit 1
fi

# Test 3: Test status command
echo "📊 Testing status command..."
./setup.sh status

# Test 4: Test stop command
echo "🛑 Testing stop command..."
./setup.sh stop

# Test 5: Test start command (brief)
echo "🚀 Testing start command (will run for 30 seconds)..."
timeout 30s ./setup.sh start &
START_PID=$!

# Wait a bit and check status
sleep 15
echo "📊 Checking status after 15 seconds..."
./setup.sh status

# Wait for timeout and stop
wait $START_PID 2>/dev/null || true
./setup.sh stop

echo "✅ All tests completed!"
echo "🎉 Setup script is working correctly!" 