# Docker Setup Guide for Dionysus

This guide will help you set up and run Dionysus using Docker Desktop.

## Prerequisites

1. **Docker Desktop** installed and running
2. **API Keys** for the required services (see below)

## Required API Keys

Before starting, you'll need to obtain the following API keys:

### 1. OpenAI API Key
- Visit [OpenAI Platform](https://platform.openai.com/api-keys)
- Create a new API key
- Used for AI-powered code analysis and documentation

### 2. Weaviate API Key
- Visit [Weaviate Cloud](https://console.weaviate.cloud/)
- Create a free account and get your API key
- Used for vector database storage

### 3. AssemblyAI Token
- Visit [AssemblyAI](https://www.assemblyai.com/)
- Sign up and get your API token
- Used for meeting transcription

### 4. GitHub Personal Access Token
- Visit [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
- Generate a new token with `repo` permissions
- Used for repository integration

### 5. Notion API Key
- Visit [Notion Developers](https://developers.notion.com/)
- Create an integration and get your API key
- Used for documentation integration

## Quick Start

### Option 1: Automated Setup (Recommended)

1. **Run the setup script:**
   ```bash
   ./setup-docker.sh
   ```

2. **Follow the prompts** to configure your environment variables

3. **Edit the `.env` file** with your API keys

4. **Run the script again** to start the services

### Option 2: Manual Setup

1. **Create environment file:**
   ```bash
   cp env.example .env
   ```

2. **Edit `.env` file** with your API keys:
   ```bash
   nano .env
   # or
   code .env
   ```

3. **Build and start containers:**
   ```bash
   docker-compose up --build -d
   ```

## Accessing the Application

Once the containers are running, you can access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8008
- **Database**: localhost:5432

## Useful Docker Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f frontend
docker-compose logs -f backend

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# Rebuild and start
docker-compose up --build -d

# Remove all containers and volumes
docker-compose down -v
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   - Check if ports 3000, 8008, or 5432 are already in use
   - Stop conflicting services or modify ports in `docker-compose.yml`

2. **API key errors:**
   - Ensure all API keys in `.env` are valid and have proper permissions
   - Check the logs for specific error messages

3. **Database connection issues:**
   - Wait a few minutes for PostgreSQL to fully start
   - Check if the database container is running: `docker-compose ps`

4. **Build failures:**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild: `docker-compose up --build --force-recreate`

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## Development Mode

For development, the containers are configured with volume mounts for hot reloading:

- Frontend changes will automatically reload
- Backend changes require container restart: `docker-compose restart backend`

## Production Considerations

For production deployment:

1. Use proper secrets management
2. Configure HTTPS
3. Set up proper database backups
4. Use production-grade PostgreSQL
5. Configure proper logging and monitoring

## Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify all API keys are correct
3. Ensure Docker Desktop has sufficient resources allocated
4. Check if all required ports are available 