import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import hashlib
import random
import string

# Initialize stemmer and stopwords
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    Preprocess text for spam detection model
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords and stem
    stemmed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    
    return ' '.join(stemmed_tokens)

def extract_features(text):
    """
    Extract features from text for spam detection model
    """
    # This is a placeholder for feature extraction
    # In a real application, you would implement more sophisticated feature extraction
    # such as TF-IDF, word embeddings, etc.
    
    features = {}
    
    # Count occurrences of common spam words
    spam_indicators = ['free', 'win', 'winner', 'cash', 'prize', 'offer', 'credit', 'loan', 'click', 'urgent']
    for word in spam_indicators:
        features[f'contains_{word}'] = 1 if word in text.lower() else 0
    
    # Check for excessive punctuation
    features['excessive_punctuation'] = 1 if len(re.findall(r'[!?]', text)) > 3 else 0
    
    # Check for all caps words
    features['has_all_caps'] = 1 if re.search(r'\b[A-Z]{3,}\b', text) else 0
    
    # Check for URLs
    features['has_url'] = 1 if re.search(r'https?://\S+|www\.\S+', text) else 0
    
    # Check for currency symbols
    features['has_currency'] = 1 if re.search(r'[$€£¥]', text) else 0
    
    # Check for numbers
    features['has_numbers'] = 1 if re.search(r'\d', text) else 0
    
    return features

def generate_password_hash(password):
    """
    Generate a secure hash for a password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, password):
    """
    Verify a password against its stored hash
    """
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()

def generate_secure_token(length=32):
    """
    Generate a secure random token
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_email(email):
    """
    Validate email format
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_url(url):
    """
    Validate URL format
    """
    url_regex = r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([/\w \.-]*)*\/?$'
    return re.match(url_regex, url) is not None

def sanitize_input(text):
    """
    Sanitize user input to prevent XSS attacks
    """
    # Replace < and > with their HTML entities
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    return text