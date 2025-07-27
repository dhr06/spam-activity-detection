-- Users table to store user information
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Scan history table to store user scan results
CREATE TABLE IF NOT EXISTS scan_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    scan_type ENUM('email', 'message', 'url') NOT NULL,
    content TEXT NOT NULL,
    is_threat BOOLEAN NOT NULL,
    threat_type VARCHAR(50) NULL,
    confidence_score FLOAT NOT NULL,
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Threat database for known threats
CREATE TABLE IF NOT EXISTS threat_database (
    id INT AUTO_INCREMENT PRIMARY KEY,
    threat_type VARCHAR(50) NOT NULL,
    pattern VARCHAR(255) NOT NULL,
    description TEXT,
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert some initial threat patterns
INSERT INTO threat_database (threat_type, pattern, description, severity) VALUES
('phishing', 'bank account.*verify', 'Phishing attempt asking to verify bank details', 'high'),
('spam', 'viagra|cialis', 'Common pharmaceutical spam', 'low'),
('malware', 'attachment.*exe|zip.*password', 'Potential malware in attachment', 'critical'),
('scam', 'lottery|winner|prize|claim', 'Common lottery or prize scam', 'medium'),
('phishing', 'password.*expired|security.*update', 'Account security update phishing', 'high');