# Developer Guide - Medical AI Assistant

## Architecture Overview

### Frontend Architecture
- **Pure JavaScript**: No frameworks, vanilla JS for maximum compatibility
- **Responsive Design**: Mobile-first approach
- **RESTful API Communication**: Fetch API for backend communication
- **Local Storage**: JWT token storage for authentication

### Backend Architecture
- **Flask Framework**: Lightweight Python web framework
- **SQLite Database**: File-based database for simplicity
- **JWT Authentication**: Secure token-based auth
- **Modular Design**: Separate modules for each AI feature

### AI Models Architecture
- **Skin Analyzer**: CNN-based image classification
- **Lab Analyzer**: OCR + Rule-based analysis
- **Chatbot**: NLP-based symptom analysis
- **Sound Analyzer**: Audio feature extraction + classification

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Analysis
- `POST /api/analyze/skin` - Analyze skin image
- `POST /api/analyze/lab` - Analyze lab report
- `POST /api/analyze/sound` - Analyze audio recording
- `POST /api/chatbot` - Chat with AI

### Records
- `GET /api/records` - Get all health records
- `GET /api/dashboard/stats` - Get dashboard statistics

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    age INTEGER,
    address TEXT,
    profile_image TEXT,
    google_id TEXT,
    created_at TIMESTAMP
);
```

### Health Records Table
```sql
CREATE TABLE health_records (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    record_type TEXT,
    diagnosis TEXT,
    treatment TEXT,
    severity TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Chat History Table
```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    message TEXT,
    response TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Adding New Features

### Adding a New Analysis Type

1. **Create Model Class** (`backend/models/new_analyzer.py`):
```python
class NewAnalyzer:
    def __init__(self):
        self.model_path = 'models_pretrained/new_model.h5'
        self.load_model()
    
    def analyze(self, input_data):
        # Your analysis logic
        return result
```

2. **Add API Endpoint** (`backend/app.py`):
```python
@app.route('/api/analyze/new', methods=['POST'])
@token_required
def analyze_new(current_user_id):
    # Handle request
    result = new_analyzer.analyze(data)
    return jsonify(result)
```

3. **Create Frontend Page** (`frontend/new-analysis.html`)

4. **Update Navigation** in all HTML files

## Testing

### Manual Testing
1. Start the application
2. Test each feature manually
3. Check browser console for errors
4. Verify database entries

### API Testing with curl
```bash
# Register
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

## Deployment

### Local Deployment
1. Run `setup.bat`
2. Run `run.bat`

### Docker Deployment
```bash
docker build -t medical-ai .
docker run -p 5000:5000 medical-ai
```

### Production Deployment
1. Change SECRET_KEY in .env
2. Set FLASK_ENV=production
3. Use production-grade server (Gunicorn)
4. Set up HTTPS
5. Use production database (PostgreSQL)

## Performance Optimization

### Frontend
- Minimize HTTP requests
- Compress images
- Use CDN for static files
- Implement caching

### Backend
- Use database indexing
- Implement request caching
- Optimize AI model inference
- Use async processing for heavy tasks

## Security Best Practices

1. **Never commit sensitive data**
2. **Use environment variables**
3. **Validate all inputs**
4. **Sanitize user uploads**
5. **Implement rate limiting**
6. **Use HTTPS in production**
7. **Regular security audits**

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small

### JavaScript
- Use ES6+ features
- Use const/let (not var)
- Write comments
- Keep functions pure when possible

### HTML/CSS
- Semantic HTML
- BEM naming convention
- Mobile-first design
- Accessibility compliance

## Troubleshooting Development Issues

### Virtual Environment Issues
```cmd
# Recreate venv
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Database Issues
```cmd
# Reset database
del medical_assistant.db
python backend/setup_project.py
```

### Port Conflicts
Change port in `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- TensorFlow: https://www.tensorflow.org/
- PyTorch: https://pytorch.org/
- OpenCV: https://opencv.org/
