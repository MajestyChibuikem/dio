# Local Weaviate Setup

This guide will help you set up Weaviate locally for the Dionysus project.

## 🚀 Quick Start

1. **Start Weaviate:**
   ```bash
   ./setup-weaviate.sh
   ```

2. **Test the connection:**
   ```bash
   python test_local_weaviate.py
   ```

3. **Start your backend:**
   ```bash
   python main.py
   ```

## 📋 Prerequisites

- Docker installed and running
- Python 3.8+ with required packages
- Environment variables set (see `env.example`)

## 🔧 Manual Setup

If the quick start doesn't work, you can set up manually:

1. **Start Weaviate container:**
   ```bash
   docker-compose -f weaviate-docker-compose.yml up -d
   ```

2. **Check if Weaviate is running:**
   ```bash
   curl http://localhost:8080/v1/.well-known/ready
   ```

3. **Access Weaviate console:**
   Open http://localhost:8080/v1/console in your browser

## 🛠️ Troubleshooting

### Weaviate won't start
- Check if Docker is running: `docker info`
- Check if port 8080 is available: `lsof -i :8080`
- View logs: `docker-compose -f weaviate-docker-compose.yml logs -f`

### Connection errors
- Make sure Weaviate is running: `curl http://localhost:8080/v1/.well-known/ready`
- Check if the collection exists in the Weaviate console
- Restart Weaviate: `docker-compose -f weaviate-docker-compose.yml restart`

### Environment variables
- Make sure `OPENAI_API_KEY` is set in your `.env` file
- The Weaviate container will use this for OpenAI integration

## 🎯 Useful Commands

```bash
# Start Weaviate
./setup-weaviate.sh

# Stop Weaviate
docker-compose -f weaviate-docker-compose.yml down

# View logs
docker-compose -f weaviate-docker-compose.yml logs -f

# Test connection
python test_local_weaviate.py

# Restart Weaviate
docker-compose -f weaviate-docker-compose.yml restart
```

## 🔄 Migration from Cloud Weaviate

The code has been updated to use local Weaviate instead of the cloud instance:

- **Before:** `https://asia-southeast1-gcp-free.weaviate.network`
- **After:** `http://localhost:8080`

This eliminates the need for cloud authentication and provides better control over your data.

## 📊 What's Different

- **No authentication required** - Local instance uses anonymous access
- **Automatic collection creation** - The code will create the `chatpdf` collection if it doesn't exist
- **Local data persistence** - Data is stored in a Docker volume
- **OpenAI integration** - Still uses your OpenAI API key for embeddings 