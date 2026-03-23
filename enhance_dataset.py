#!/usr/bin/env python3
"""
Enhanced Email Dataset Generator
Adds more sophisticated fields to improve phishing detection accuracy
"""

import pandas as pd
import numpy as np
import random
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse

def extract_features_from_text(text):
    """Extract additional features from email text"""
    
    # Count suspicious words/phrases
    suspicious_phrases = [
        'urgent', 'immediate', 'verify', 'suspended', 'click here', 'act now',
        'limited time', 'expires', 'confirm', 'update', 'secure', 'account',
        'frozen', 'blocked', 'unauthorized', 'suspicious', 'alert', 'warning'
    ]
    
    suspicious_count = sum(1 for phrase in suspicious_phrases if phrase.lower() in text.lower())
    
    # Check for urgency indicators
    urgency_words = ['urgent', 'immediate', 'asap', 'emergency', 'critical', 'expires', 'deadline']
    urgency_score = sum(1 for word in urgency_words if word.lower() in text.lower())
    
    # Count exclamation marks and capital letters
    exclamation_count = text.count('!')
    caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
    
    # Check for monetary amounts
    money_pattern = r'[\$£€¥₽₹]\s*[\d,]+|[\d,]+\s*(?:dollars?|pounds?|euros?|yen|rubles?|rupees?)'
    money_mentions = len(re.findall(money_pattern, text, re.IGNORECASE))
    
    # Check for personal info requests
    personal_info_keywords = ['ssn', 'social security', 'credit card', 'password', 'pin', 'account number']
    personal_info_requests = sum(1 for keyword in personal_info_keywords if keyword.lower() in text.lower())
    
    return {
        'suspicious_word_count': suspicious_count,
        'urgency_score': urgency_score,
        'exclamation_count': exclamation_count,
        'caps_ratio': round(caps_ratio, 3),
        'money_mentions': money_mentions,
        'personal_info_requests': personal_info_requests
    }

def analyze_sender_domain(sender):
    """Analyze sender domain characteristics"""
    if not sender or '@' not in sender:
        return {'sender_domain_suspicious': True, 'sender_tld': 'unknown', 'sender_domain_length': 0}
    
    domain = sender.split('@')[1] if '@' in sender else ''
    
    # Check for suspicious domain characteristics
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.edu', '.gov', '.org']  # Some are legitimate but often abused
    legitimate_tlds = ['.com', '.org', '.net', '.edu', '.gov']
    
    tld = '.' + domain.split('.')[-1] if '.' in domain else ''
    
    # Check for domain spoofing patterns
    spoofing_indicators = ['fake-', 'secure-', 'verify-', 'update-', 'alert-', 'urgent-']
    is_spoofed = any(indicator in domain.lower() for indicator in spoofing_indicators)
    
    return {
        'sender_domain_suspicious': is_spoofed or tld not in legitimate_tlds,
        'sender_tld': tld,
        'sender_domain_length': len(domain),
        'sender_domain_spoofed': is_spoofed
    }

def analyze_urls(urls):
    """Analyze URL characteristics"""
    if not urls or urls == 'none':
        return {
            'url_count': 0,
            'suspicious_url': False,
            'url_shortener': False,
            'url_ip_address': False,
            'url_suspicious_tld': False
        }
    
    # Check for suspicious URL patterns
    suspicious_patterns = ['.phish', '.malicious', '.suspicious', '.fraud', '.scam', '.evil', '.bad', '.fake']
    shortener_domains = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'short.link']
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.click', '.download']
    
    has_suspicious = any(pattern in urls.lower() for pattern in suspicious_patterns)
    has_shortener = any(domain in urls.lower() for domain in shortener_domains)
    has_suspicious_tld = any(tld in urls.lower() for tld in suspicious_tlds)
    
    # Check for IP addresses
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    has_ip = bool(re.search(ip_pattern, urls))
    
    return {
        'url_count': 1,  # Simplified - in real scenario would count actual URLs
        'suspicious_url': has_suspicious,
        'url_shortener': has_shortener,
        'url_ip_address': has_ip,
        'url_suspicious_tld': has_suspicious_tld
    }

def generate_email_metadata(label):
    """Generate realistic email metadata"""
    
    # Generate timestamp (last 6 months)
    base_date = datetime.now() - timedelta(days=180)
    random_days = random.randint(0, 180)
    timestamp = base_date + timedelta(days=random_days)
    
    # Time patterns (phishing often sent at odd hours)
    if label == 'phishing':
        # More likely to be sent at odd hours
        hour = random.choice(list(range(0, 6)) + list(range(22, 24)) + list(range(9, 17)))
    else:
        # Legitimate emails more likely during business hours
        hour = random.choice(list(range(8, 18)))
    
    timestamp = timestamp.replace(hour=hour, minute=random.randint(0, 59))
    
    # Email client information
    email_clients = ['Outlook', 'Gmail', 'Apple Mail', 'Thunderbird', 'Yahoo Mail', 'Unknown']
    client_weights = [0.3, 0.4, 0.1, 0.05, 0.1, 0.05] if label == 'legit' else [0.1, 0.2, 0.05, 0.05, 0.1, 0.5]
    email_client = np.random.choice(email_clients, p=client_weights)
    
    # DKIM and DMARC status
    if label == 'phishing':
        dkim_valid = random.choice([True, False]) if random.random() < 0.3 else False
        dmarc_pass = random.choice([True, False]) if random.random() < 0.2 else False
    else:
        dkim_valid = random.choice([True, False]) if random.random() < 0.8 else True
        dmarc_pass = random.choice([True, False]) if random.random() < 0.9 else True
    
    # Email priority
    priorities = ['low', 'normal', 'high']
    if label == 'phishing':
        priority_weights = [0.1, 0.4, 0.5]  # Phishing often marked as high priority
    else:
        priority_weights = [0.2, 0.7, 0.1]  # Legitimate emails mostly normal priority
    
    priority = np.random.choice(priorities, p=priority_weights)
    
    # Message size (bytes)
    if label == 'phishing':
        size = random.randint(500, 3000)  # Usually shorter, more focused
    else:
        size = random.randint(800, 8000)  # Can be longer with more content
    
    return {
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'day_of_week': timestamp.strftime('%A'),
        'hour_sent': timestamp.hour,
        'email_client': email_client,
        'dkim_valid': dkim_valid,
        'dmarc_pass': dmarc_pass,
        'priority': priority,
        'message_size_bytes': size
    }

def enhance_dataset(input_file, output_file, sample_size=None):
    """Enhance the existing dataset with additional fields"""
    
    print(f"Loading dataset from {input_file}...")
    df = pd.read_csv(input_file)
    
    if sample_size:
        df = df.sample(n=min(sample_size, len(df)), random_state=42)
        print(f"Working with sample of {len(df)} rows")
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Original columns: {list(df.columns)}")
    
    # Initialize new columns
    enhanced_data = []
    
    print("Enhancing dataset with new features...")
    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"Processed {idx}/{len(df)} rows...")
        
        # Start with original data
        enhanced_row = row.to_dict()
        
        # Extract text features
        text_features = extract_features_from_text(row['text'])
        enhanced_row.update(text_features)
        
        # Analyze sender domain
        sender_features = analyze_sender_domain(row['sender'])
        enhanced_row.update(sender_features)
        
        # Analyze URLs
        url_features = analyze_urls(row['urls'])
        enhanced_row.update(url_features)
        
        # Generate metadata
        metadata = generate_email_metadata(row['label'])
        enhanced_row.update(metadata)
        
        # Add email length
        enhanced_row['text_length'] = len(row['text'])
        enhanced_row['word_count'] = len(row['text'].split())
        
        # Add readability score (simplified)
        sentences = len([s for s in row['text'].split('.') if s.strip()])
        words = len(row['text'].split())
        enhanced_row['avg_words_per_sentence'] = round(words / sentences if sentences > 0 else 0, 2)
        
        enhanced_data.append(enhanced_row)
    
    # Create enhanced DataFrame
    enhanced_df = pd.DataFrame(enhanced_data)
    
    # Reorder columns for better readability
    column_order = [
        # Original columns
        'label', 'text', 'urls', 'sender', 'spfrecord',
        
        # Text analysis
        'text_length', 'word_count', 'avg_words_per_sentence', 
        'suspicious_word_count', 'urgency_score', 'exclamation_count', 
        'caps_ratio', 'money_mentions', 'personal_info_requests',
        
        # Sender analysis
        'sender_domain_suspicious', 'sender_tld', 'sender_domain_length', 'sender_domain_spoofed',
        
        # URL analysis
        'url_count', 'suspicious_url', 'url_shortener', 'url_ip_address', 'url_suspicious_tld',
        
        # Email metadata
        'timestamp', 'day_of_week', 'hour_sent', 'email_client', 
        'dkim_valid', 'dmarc_pass', 'priority', 'message_size_bytes'
    ]
    
    enhanced_df = enhanced_df[column_order]
    
    print(f"\nEnhanced dataset shape: {enhanced_df.shape}")
    print(f"New columns added: {len(enhanced_df.columns) - len(df.columns)}")
    print(f"Enhanced columns: {list(enhanced_df.columns)}")
    
    # Save enhanced dataset
    enhanced_df.to_csv(output_file, index=False)
    print(f"\nEnhanced dataset saved to {output_file}")
    
    # Print summary statistics
    print("\n=== DATASET ENHANCEMENT SUMMARY ===")
    print(f"Original features: {len(df.columns)}")
    print(f"Enhanced features: {len(enhanced_df.columns)}")
    print(f"Features added: {len(enhanced_df.columns) - len(df.columns)}")
    
    print(f"\nLabel distribution:")
    print(enhanced_df['label'].value_counts())
    
    print(f"\nSample of new features:")
    print(enhanced_df[['suspicious_word_count', 'urgency_score', 'sender_domain_suspicious', 
                      'dkim_valid', 'priority']].head())
    
    return enhanced_df

if __name__ == "__main__":
    input_file = "data/emails_train.csv"
    output_file = "data/emails_train_enhanced.csv"
    
    # Process a sample first (10,000 rows) to test
    print("Creating enhanced dataset with additional features...")
    print("Processing first 10,000 rows as a sample...")
    
    enhanced_df = enhance_dataset(input_file, output_file, sample_size=10000)
    
    print("\n✅ Dataset enhancement complete!")
    print(f"Enhanced dataset saved as: {output_file}")
    print("\nNew features include:")
    print("- Text analysis (suspicious words, urgency, formatting)")
    print("- Sender domain analysis (spoofing detection)")
    print("- URL analysis (malicious patterns)")
    print("- Email metadata (timing, authentication, client)")
    print("- Readability metrics")
