#!/bin/bash

echo "🔧 Setting up environment variables"
echo "=================================="

# Create .env file for webapp
echo "📝 Creating .env file for webapp..."
cat > webapp/.env << EOF
# Database URL for Prisma
DATABASE_URL="postgresql://dionysus:dionysus_password@localhost:5432/dionysus"

# Node environment
NODE_ENV="development"

# Skip environment validation for development
SKIP_ENV_VALIDATION="true"
EOF

echo "✅ Environment file created: webapp/.env"
echo ""
echo "📋 Environment variables set:"
echo "   - DATABASE_URL: postgresql://dionysus:dionysus_password@localhost:5432/dionysus"
echo "   - NODE_ENV: development"
echo "   - SKIP_ENV_VALIDATION: true"
echo ""
echo "🚀 You can now run: ./start-frontend.sh" 