#!/bin/bash

echo "🚀 Setting up Dionysus to run locally on your laptop"
echo "=================================================="
echo "📝 Note: This will use your system Python (3.10.11) and install dependencies locally"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if Bun is available
if ! command -v bun &> /dev/null; then
    echo "⚠️  Bun is not installed. Installing Bun..."
    curl -fsSL https://bun.sh/install | bash
    source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null
fi

echo "✅ Prerequisites check passed!"
echo ""

# Set up backend
echo "🔧 Setting up Python backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Set up frontend
echo "🎨 Setting up Next.js frontend..."
cd ../webapp

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
bun install

# Generate Prisma client
echo "🗄️  Generating Prisma client..."
bunx prisma generate

echo "✅ Frontend setup complete!"
echo ""

# Create environment file if it doesn't exist
cd ..
if [ ! -f ".env" ]; then
    echo "📝 Creating environment file..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your API keys before starting the application"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 To start the application:"
echo "   1. Backend: cd backend && source venv/bin/activate && python main.py"
echo "   2. Frontend: cd webapp && bun dev"
echo ""
echo "📱 Frontend will be available at: http://localhost:3000"
echo "🔧 Backend API will be available at: http://localhost:8008"
echo ""
echo "⚠️  Don't forget to:"
echo "   - Edit .env file with your API keys"
echo "   - Set up your database (if needed)" 