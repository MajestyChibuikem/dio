#!/bin/bash

echo "🎨 Starting Dionysus Frontend"
echo "============================"

# Add Bun to PATH
export PATH="$HOME/.bun/bin:$PATH"

# Check if Bun is available
if ! command -v bun &> /dev/null; then
    echo "❌ Bun is not available. Please install Bun first."
    exit 1
fi

echo "✅ Bun found: $(which bun)"

# Navigate to webapp directory
cd webapp

echo "🚀 Starting Next.js development server..."
echo "📱 Frontend will be available at: http://localhost:3000"
echo ""

# Start the development server
bun dev 