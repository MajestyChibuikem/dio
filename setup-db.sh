#!/bin/bash

echo "🗄️  Setting up SQLite database for local development"
echo "=================================================="

# Add Bun to PATH
export PATH="$HOME/.bun/bin:$PATH"

# Navigate to webapp directory
cd webapp

echo "🔧 Generating Prisma client..."
bunx prisma generate

echo "🗄️  Pushing database schema..."
bunx prisma db push

echo "✅ Database setup complete!"
echo ""
echo "🚀 You can now run the frontend without database errors:"
echo "   ./start-frontend.sh" 