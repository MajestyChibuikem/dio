# Dionysuss All-in-One Setup Script

This script provides a complete solution for setting up and managing the entire Dionysuss application stack.

## 🚀 Quick Start

```bash
# Start everything (Weaviate + Backend + Frontend)
./setup.sh start

# Or simply run (start is the default)
./setup.sh
```

## 📋 Commands

### Start All Services
```bash
./setup.sh start
```
- Sets up Python environment
- Installs Node.js dependencies
- Starts Weaviate container
- Starts backend server
- Starts frontend server
- Shows status and URLs

### Stop All Services
```bash
./setup.sh stop
```
- Stops frontend server
- Stops backend server
- Stops Weaviate container

### Restart All Services
```bash
./setup.sh restart
```
- Stops all services
- Starts all services fresh

### Check Status
```bash
./setup.sh status
```
- Shows which services are running
- Displays access URLs

### Clear All Data
```bash
./setup.sh clean
```
- Stops all services
- Clears frontend database
- Clears Weaviate database
- Removes all project data

## 🔧 What the Script Does

### 1. Environment Setup
- ✅ Checks for Python 3.13.5 (uses pyenv if available)
- ✅ Installs Python dependencies from `backend/requirements.txt`
- ✅ Checks for Node.js
- ✅ Installs Node.js dependencies from `webapp/package.json`

### 2. Weaviate Setup
- ✅ Checks for Docker and Docker Compose
- ✅ Copies `.env` file to backend directory
- ✅ Starts Weaviate container
- ✅ Creates database schema
- ✅ Waits for service to be ready

### 3. Backend Setup
- ✅ Kills any existing backend process
- ✅ Starts backend server on port 8008
- ✅ Waits for service to be ready

### 4. Frontend Setup
- ✅ Kills any existing frontend process
- ✅ Starts frontend server on port 3000
- ✅ Waits for service to be ready

## 🌐 Access URLs

Once running, you can access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8008
- **Weaviate**: http://localhost:8080

## 📁 File Structure

The script creates these files:
- `backend.pid` - Backend process ID
- `frontend.pid` - Frontend process ID
- `backend.log` - Backend server logs
- `frontend.log` - Frontend server logs

## 🛠️ Prerequisites

Make sure you have:
- ✅ Python 3.13.5 (or later)
- ✅ Node.js 18+ (or later)
- ✅ Docker Desktop
- ✅ Docker Compose
- ✅ `.env` file with API keys

## 🔍 Troubleshooting

### Port Already in Use
The script automatically kills processes using required ports (3000, 8008, 8080).

### Docker Not Running
Make sure Docker Desktop is started before running the script.

### Missing Dependencies
The script will show clear error messages if any required software is missing.

### Clean Start
If you encounter issues, try:
```bash
./setup.sh clean
./setup.sh start
```

## 🎯 Usage Examples

```bash
# Start everything
./setup.sh

# Check what's running
./setup.sh status

# Stop everything
./setup.sh stop

# Restart everything
./setup.sh restart

# Clear all data and start fresh
./setup.sh clean
./setup.sh start
```

## 📝 Notes

- The script runs continuously when started (keeps services alive)
- Press `Ctrl+C` to stop all services
- Logs are saved to `backend.log` and `frontend.log`
- The script handles cleanup automatically on exit 