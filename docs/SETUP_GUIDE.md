# Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - Download from [python.org](https://www.python.org)
- **Node.js 14 or higher** - Download from [nodejs.org](https://nodejs.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)
- **Virtual Environment** - Using Python's built-in `venv`

Verify installations:
```bash
python --version
node --version
npm --version
git --version
```

## Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
# nano .env  # or use your preferred editor
```

### Step 5: Create Data Directories
```bash
mkdir -p models
mkdir -p logs
```

### Step 6: Initialize RAG System (Optional)
If you want to pre-build the vector database:
```bash
python -c "from rag_system.waste_rag import WasteRAG; WasteRAG()"
```

### Step 7: Run Backend Server
```bash
python app.py
```

The server will start at `http://localhost:5000`

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

Test the health endpoint:
```bash
curl http://localhost:5000/health
```

## Frontend Setup

### Step 1: Open New Terminal Window
Leave the backend running and open a new terminal.

### Step 2: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 3: Install Dependencies
```bash
npm install
```

### Step 4: Configure Environment Variables
```bash
# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000" > .env
```

### Step 5: Start Development Server
```bash
npm start
```

The application will open automatically at `http://localhost:3000`

**Expected Output:**
```
compiled successfully!
```

## Verification Checklist

- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Health endpoint responding at `/health`
- [ ] Camera permission dialog appears in browser
- [ ] Able to upload test image

## Common Issues & Solutions

### Issue: "Python not found" or "command not found"
**Solution:**
- On macOS/Linux, try `python3` instead of `python`
- Ensure Python is added to your PATH environment variable

### Issue: "pip install" fails with permission error
**Solution:**
```bash
pip install --user -r requirements.txt
```

### Issue: Port 5000 or 3000 already in use
**Solution:**
```bash
# Change port in .env or use:
FLASK_PORT=5001  # for backend
# Then update frontend's REACT_APP_API_URL accordingly
```

### Issue: "Cannot find module" errors in frontend
**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: Camera not working in browser
**Solution:**
- Check browser permissions for camera access
- Use HTTPS in production (browsers require HTTPS for camera access)
- Test on a different browser if available

### Issue: CORS errors when backend calls frontend
**Solution:**
Ensure the backend's CORS configuration matches:
```python
CORS_ORIGINS=http://localhost:3000
```

## Docker Setup (Alternative)

### Build and Run with Docker Compose

```bash
# From project root
docker-compose up --build
```

This will:
1. Build the backend image
2. Build the frontend image
3. Start both services
4. Access the app at `http://localhost:3000`

### Individual Docker Commands

**Backend:**
```bash
docker build -f Dockerfile.backend -t waste-sorter-backend .
docker run -p 5000:5000 waste-sorter-backend
```

**Frontend:**
```bash
cd frontend
docker build -t waste-sorter-frontend .
docker run -p 3000:3000 waste-sorter-frontend
```

## Testing the Application

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Accessing the Application

Once both services are running:

1. **Main Application**: [http://localhost:3000](http://localhost:3000)
2. **API Endpoint**: [http://localhost:5000](http://localhost:5000)
3. **API Health Check**: [http://localhost:5000/health](http://localhost:5000/health)

## Next Steps

1. **Upload a test image** to verify classification is working
2. **Test different regions** to see regional regulations
3. **Review the API documentation** in `docs/API_DOCUMENTATION.md`
4. **Explore the code** and understand the architecture

## Development Workflow

### Making Changes

**Backend:**
1. Edit Python files in `backend/`
2. Flask will auto-reload changes in development mode
3. Test with curl or Postman

**Frontend:**
1. Edit React components in `frontend/src/`
2. Changes auto-refresh in browser
3. Check console for errors

### Code Quality

**Backend:**
```bash
# Format code
black backend/

# Lint
flake8 backend/
```

**Frontend:**
```bash
# Check for errors
npm run build
```

## Production Deployment

### Before Going Live

- [ ] Set `FLASK_ENV=production`
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Add authentication and API keys
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up proper logging and monitoring
- [ ] Configure rate limiting
- [ ] Test with various image sizes
- [ ] Optimize model for inference speed

### Deployment Options

- **Heroku**: Add Procfile and buildpacks
- **AWS**: EC2, ECS, or Lambda
- **Google Cloud**: App Engine or Cloud Run
- **Azure**: App Service
- **DigitalOcean**: App Platform

See `docs/DEPLOYMENT.md` for detailed instructions.

## Getting Help

- Check the main [README.md](../README.md) for overview
- Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for endpoints
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Create an issue in the repository
