from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from database.db import init_db, get_db
from models.skin_analyzer import SkinAnalyzer
from models.lab_analyzer import LabAnalyzer
from models.chatbot import MedicalChatbot
from models.sound_analyzer import SoundAnalyzer
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

CORS(app)

# Initialize database
init_db()

# Initialize AI models
skin_analyzer = SkinAnalyzer()
lab_analyzer = LabAnalyzer()
chatbot = MedicalChatbot()
sound_analyzer = SoundAnalyzer()

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            token = token.split()[1] if ' ' in token else token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

# Routes - Frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Routes - Authentication
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    db = get_db()
    
    # Check if user exists
    existing_user = db.execute(
        'SELECT id FROM users WHERE email = ?', (data['email'],)
    ).fetchone()
    
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user
    hashed_password = generate_password_hash(data['password'])
    db.execute(
        'INSERT INTO users (email, password, name, age, address) VALUES (?, ?, ?, ?, ?)',
        (data['email'], hashed_password, data.get('name', ''), 
         data.get('age', 0), data.get('address', ''))
    )
    db.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    
    user = db.execute(
        'SELECT * FROM users WHERE email = ?', (data['email'],)
    ).fetchone()
    
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.utcnow() + timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name']
        }
    })

# Routes - Profile
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    db = get_db()
    user = db.execute(
        'SELECT id, email, name, age, address, profile_image FROM users WHERE id = ?',
        (current_user_id,)
    ).fetchone()
    
    return jsonify(dict(user))

@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile(current_user_id):
    data = request.json
    db = get_db()
    
    db.execute(
        'UPDATE users SET name = ?, age = ?, address = ? WHERE id = ?',
        (data.get('name'), data.get('age'), data.get('address'), current_user_id)
    )
    db.commit()
    
    return jsonify({'message': 'Profile updated successfully'})

# Routes - Skin Analysis
@app.route('/api/analyze/skin', methods=['POST'])
@token_required
def analyze_skin(current_user_id):
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'skin_{current_user_id}_{datetime.now().timestamp()}.jpg')
    file.save(filepath)
    
    # Analyze image
    result = skin_analyzer.analyze(filepath)
    
    # Save to database
    db = get_db()
    db.execute(
        'INSERT INTO health_records (user_id, record_type, diagnosis, treatment, severity) VALUES (?, ?, ?, ?, ?)',
        (current_user_id, 'skin', result['diagnosis'], result['treatment'], result['severity'])
    )
    db.commit()
    
    return jsonify(result)

# Routes - Lab Analysis
@app.route('/api/analyze/lab', methods=['POST'])
@token_required
def analyze_lab(current_user_id):
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'lab_{current_user_id}_{datetime.now().timestamp()}.jpg')
    file.save(filepath)
    
    result = lab_analyzer.analyze(filepath)
    
    db = get_db()
    db.execute(
        'INSERT INTO health_records (user_id, record_type, diagnosis, treatment, severity) VALUES (?, ?, ?, ?, ?)',
        (current_user_id, 'lab', result['diagnosis'], result['treatment'], result['severity'])
    )
    db.commit()
    
    return jsonify(result)

# Routes - Chatbot
@app.route('/api/chatbot', methods=['POST'])
@token_required
def chat(current_user_id):
    data = request.json
    message = data.get('message', '')
    
    response = chatbot.get_response(message)
    
    db = get_db()
    db.execute(
        'INSERT INTO chat_history (user_id, message, response) VALUES (?, ?, ?)',
        (current_user_id, message, response)
    )
    db.commit()
    
    return jsonify({'response': response})

# Routes - Sound Analysis
@app.route('/api/analyze/sound', methods=['POST'])
@token_required
def analyze_sound(current_user_id):
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'sound_{current_user_id}_{datetime.now().timestamp()}.wav')
    file.save(filepath)
    
    result = sound_analyzer.analyze(filepath)
    
    db = get_db()
    db.execute(
        'INSERT INTO health_records (user_id, record_type, diagnosis, treatment, severity) VALUES (?, ?, ?, ?, ?)',
        (current_user_id, 'sound', result['diagnosis'], result['treatment'], result['severity'])
    )
    db.commit()
    
    return jsonify(result)

# Routes - Health Records
@app.route('/api/records', methods=['GET'])
@token_required
def get_records(current_user_id):
    db = get_db()
    records = db.execute(
        'SELECT * FROM health_records WHERE user_id = ? ORDER BY created_at DESC',
        (current_user_id,)
    ).fetchall()
    
    return jsonify([dict(record) for record in records])

# Routes - Dashboard Stats
@app.route('/api/dashboard/stats', methods=['GET'])
@token_required
def get_dashboard_stats(current_user_id):
    db = get_db()
    
    stats = {
        'total_analyses': db.execute(
            'SELECT COUNT(*) as count FROM health_records WHERE user_id = ?',
            (current_user_id,)
        ).fetchone()['count'],
        'skin_analyses': db.execute(
            'SELECT COUNT(*) as count FROM health_records WHERE user_id = ? AND record_type = ?',
            (current_user_id, 'skin')
        ).fetchone()['count'],
        'lab_analyses': db.execute(
            'SELECT COUNT(*) as count FROM health_records WHERE user_id = ? AND record_type = ?',
            (current_user_id, 'lab')
        ).fetchone()['count'],
        'sound_analyses': db.execute(
            'SELECT COUNT(*) as count FROM health_records WHERE user_id = ? AND record_type = ?',
            (current_user_id, 'sound')
        ).fetchone()['count'],
        'recent_records': [dict(r) for r in db.execute(
            'SELECT * FROM health_records WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
            (current_user_id,)
        ).fetchall()]
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    print("=" * 50)
    print("Medical AI Assistant Server")
    print("=" * 50)
    print("Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
