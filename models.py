import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os
from config import Config

class SpamDetectionModel:
    def __init__(self, model_type='naive_bayes'):
        self.model_type = model_type
        self.vectorizer = TfidfVectorizer(max_features=5000)
        
        if model_type == 'naive_bayes':
            self.model = MultinomialNB()
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_type == 'svm':
            self.model = SVC(kernel='linear', probability=True, random_state=42)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def train(self, X, y):
        """
        Train the model with the provided data
        """
        # Split data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Fit the vectorizer and transform the training data
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        
        # Train the model
        self.model.fit(X_train_vectorized, y_train)
        
        # Evaluate on validation set
        X_val_vectorized = self.vectorizer.transform(X_val)
        y_pred = self.model.predict(X_val_vectorized)
        
        # Calculate metrics
        accuracy = accuracy_score(y_val, y_pred)
        precision = precision_score(y_val, y_pred, average='binary')
        recall = recall_score(y_val, y_pred, average='binary')
        f1 = f1_score(y_val, y_pred, average='binary')
        
        print(f"Model: {self.model_type}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def predict(self, texts):
        """
        Predict if texts are spam or not
        """
        # Vectorize the texts
        X_vectorized = self.vectorizer.transform(texts)
        
        # Get predictions
        predictions = self.model.predict(X_vectorized)
        
        return predictions
    
    def predict_proba(self, texts):
        """
        Get probability scores for predictions
        """
        # Vectorize the texts
        X_vectorized = self.vectorizer.transform(texts)
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(X_vectorized)
        
        return probabilities
    
    def save(self, filepath=None):
        """
        Save the model to a file
        """
        if filepath is None:
            filepath = Config.MODEL_PATH
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the model and vectorizer
        with open(filepath, 'wb') as f:
            pickle.dump({'model': self.model, 'vectorizer': self.vectorizer, 'model_type': self.model_type}, f)
        
        print(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath=None):
        """
        Load a model from a file
        """
        if filepath is None:
            filepath = Config.MODEL_PATH
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        # Load the model and vectorizer
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        # Create a new instance with the loaded model type
        instance = cls(model_type=data['model_type'])
        instance.model = data['model']
        instance.vectorizer = data['vectorizer']
        
        print(f"Model loaded from {filepath}")
        return instance


class DummyModel:
    """
    A dummy model for demonstration purposes
    """
    def predict_proba(self, texts):
        """
        Return random probabilities for demonstration
        """
        # For each text, return a random probability
        # First column is probability of not spam, second column is probability of spam
        return np.array([[np.random.uniform(0.6, 0.9), np.random.uniform(0.1, 0.4)] for _