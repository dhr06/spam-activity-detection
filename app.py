from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
import re
import pickle
import numpy as np
from config import Config
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import hashlib

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Download NLTK resources (uncomment first time)
# nltk.download('punkt')
# nltk.download('stopwords')

# Initialize stemmer and stopwords
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
    return conn

# Load AI model (dummy function - replace with actual model loading)
def load_model():
    # In a real application, you would load a trained model from a file
    # For now, we'll create a dummy model that returns random predictions
    class DummyModel:
        def predict_proba(self, X):
            # Return random probabilities for demonstration
            return np.array([[0.7, 0.3] for _ in range(len(X))])
    
    return DummyModel()

# Train model (dummy function - replace with actual training code)
def train_model(X, y):
    # In a real application, you would train a model here
    # For now, we'll just print a message
    print(f"Training model with {len(X)} samples")
    return load_model()

# Text preprocessing function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords and stem
    stemmed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    
    return ' '.join(stemmed_tokens)

# Initialize model
model = load_model()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard', 'warning')
        return redirect(url_for('login'))
    
    # Get user's scan history
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM scan_history WHERE user_id = %s ORDER BY scan_date DESC LIMIT 10",
        (session['user_id'],)
    )
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', history=history)

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        scan_type = request.form.get('scan_type')
        content = request.form.get('content')
        
        if not content:
            flash('Please provide content to scan', 'danger')
            return redirect(url_for('scan'))
        
        # Preprocess the text
        processed_text = preprocess_text(content)
        
        # Make prediction using the model
        # In a real application, you would convert the text to features first
        prediction_proba = model.predict_proba([processed_text])[0]
        is_threat = prediction_proba[1] > Config.THRESHOLD_THREAT
        confidence_score = prediction_proba[1] if is_threat else prediction_proba[0]
        
        # Determine threat type (simplified for demo)
        threat_type = None
        if is_threat:
            # Check against known patterns in the database
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT threat_type FROM threat_database")
            threat_types = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Simple pattern matching (in a real app, use more sophisticated methods)
            for threat in threat_types:
                if re.search(threat['pattern'], content, re.IGNORECASE):
                    threat_type = threat['threat_type']
                    break
            
            if not threat_type:
                threat_type = 'unknown'
        
        # Save scan result to database if user is logged in
        if 'user_id' in session:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO scan_history (user_id, scan_type, content, is_threat, threat_type, confidence_score) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (session['user_id'], scan_type, content, is_threat, threat_type, float(confidence_score))
            )
            conn.commit()
            cursor.close()
            conn.close()
        
        # Prepare result data
        result = {
            'is_threat': is_threat,
            'threat_type': threat_type,
            'confidence_score': round(confidence_score * 100, 2),
            'content': content,
            'scan_type': scan_type
        }
        
        return render_template('results.html', result=result)
    
    return render_template('scan.html')

@app.route('/scan/email', methods=['GET', 'POST'])
def scan_email():
    if request.method == 'POST':
        email_content = request.form.get('email_content')
        return redirect(url_for('scan', scan_type='email', content=email_content))
    return render_template('scan.html', scan_type='email')

@app.route('/scan/message', methods=['GET', 'POST'])
def scan_message():
    if request.method == 'POST':
        message_content = request.form.get('message_content')
        return redirect(url_for('scan', scan_type='message', content=message_content))
    return render_template('scan.html', scan_type='message')

@app.route('/scan/url', methods=['GET', 'POST'])
def scan_url():
    if request.method == 'POST':
        url_content = request.form.get('url_content')
        return redirect(url_for('scan', scan_type='url', content=url_content))
    return render_template('scan.html', scan_type='url')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password', 'danger')
            return redirect(url_for('login'))
        
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Check credentials
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password_hash = %s",
            (username, password_hash)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password or not confirm_password:
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Check if username or email already exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Username or email already exists', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.json
    if not data or 'content' not in data or 'scan_type' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    content = data['content']
    scan_type = data['scan_type']
    
    # Preprocess and predict
    processed_text = preprocess_text(content)
    prediction_proba = model.predict_proba([processed_text])[0]
    is_threat = prediction_proba[1] > Config.THRESHOLD_THREAT
    confidence_score = prediction_proba[1] if is_threat else prediction_proba[0]
    
    # Determine threat type (simplified)
    threat_type = 'unknown' if is_threat else None
    
    return jsonify({
        'is_threat': is_threat,
        'threat_type': threat_type,
        'confidence_score': round(confidence_score * 100, 2)
    })

@app.route('/chat')
def chat():
    # Uncomment the following lines if you want to require login for chat
    # if 'user_id' not in session:
    #     flash('Please log in to access the chat', 'warning')
    #     return redirect(url_for('login'))
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)