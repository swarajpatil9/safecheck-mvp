#!/usr/bin/env python3
"""
Dataset Analysis and Visualization
Analyzes the enhanced email dataset and creates visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

def analyze_enhanced_dataset(file_path):
    """Analyze the enhanced dataset and create visualizations"""
    
    print("Loading enhanced dataset...")
    df = pd.read_csv(file_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Features: {len(df.columns)}")
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create a comprehensive analysis
    fig = plt.figure(figsize=(20, 16))
    
    # 1. Label distribution
    plt.subplot(3, 4, 1)
    df['label'].value_counts().plot(kind='bar', color=['green', 'red'])
    plt.title('Email Label Distribution')
    plt.xlabel('Label')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    
    # 2. Suspicious word count distribution
    plt.subplot(3, 4, 2)
    sns.boxplot(data=df, x='label', y='suspicious_word_count')
    plt.title('Suspicious Words by Label')
    plt.xlabel('Label')
    plt.ylabel('Suspicious Word Count')
    
    # 3. Text length distribution
    plt.subplot(3, 4, 3)
    sns.histplot(data=df, x='text_length', hue='label', bins=30, alpha=0.7)
    plt.title('Text Length Distribution')
    plt.xlabel('Text Length (characters)')
    plt.ylabel('Frequency')
    
    # 4. Urgency score
    plt.subplot(3, 4, 4)
    urgency_cross = pd.crosstab(df['urgency_score'], df['label'])
    urgency_cross.plot(kind='bar', stacked=True, color=['green', 'red'])
    plt.title('Urgency Score Distribution')
    plt.xlabel('Urgency Score')
    plt.ylabel('Count')
    plt.legend(['Legit', 'Phishing'])
    
    # 5. Sender domain suspicious
    plt.subplot(3, 4, 5)
    domain_cross = pd.crosstab(df['sender_domain_suspicious'], df['label'])
    domain_cross.plot(kind='bar', color=['green', 'red'])
    plt.title('Sender Domain Suspicious')
    plt.xlabel('Domain Suspicious')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.legend(['Legit', 'Phishing'])
    
    # 6. Authentication status
    plt.subplot(3, 4, 6)
    auth_data = df.groupby(['label', 'dkim_valid']).size().unstack(fill_value=0)
    auth_data.plot(kind='bar', color=['red', 'green'])
    plt.title('DKIM Validation by Label')
    plt.xlabel('Label')
    plt.ylabel('Count')
    plt.legend(['Invalid', 'Valid'])
    plt.xticks(rotation=0)
    
    # 7. Hour sent distribution
    plt.subplot(3, 4, 7)
    hour_phishing = df[df['label'] == 'phishing']['hour_sent']
    hour_legit = df[df['label'] == 'legit']['hour_sent']
    
    plt.hist([hour_legit, hour_phishing], bins=24, alpha=0.7, 
             label=['Legit', 'Phishing'], color=['green', 'red'])
    plt.title('Email Send Time Distribution')
    plt.xlabel('Hour of Day')
    plt.ylabel('Frequency')
    plt.legend()
    
    # 8. Priority distribution
    plt.subplot(3, 4, 8)
    priority_cross = pd.crosstab(df['priority'], df['label'])
    priority_cross.plot(kind='bar', color=['green', 'red'])
    plt.title('Email Priority Distribution')
    plt.xlabel('Priority')
    plt.ylabel('Count')
    plt.legend(['Legit', 'Phishing'])
    plt.xticks(rotation=0)
    
    # 9. Money mentions
    plt.subplot(3, 4, 9)
    sns.boxplot(data=df, x='label', y='money_mentions')
    plt.title('Money Mentions by Label')
    plt.xlabel('Label')
    plt.ylabel('Money Mentions Count')
    
    # 10. Caps ratio
    plt.subplot(3, 4, 10)
    sns.boxplot(data=df, x='label', y='caps_ratio')
    plt.title('Caps Ratio by Label')
    plt.xlabel('Label')
    plt.ylabel('Uppercase Ratio')
    
    # 11. SPF record status
    plt.subplot(3, 4, 11)
    spf_cross = pd.crosstab(df['spfrecord'], df['label'])
    spf_cross.plot(kind='bar', color=['green', 'red'])
    plt.title('SPF Record Status')
    plt.xlabel('SPF Status')
    plt.ylabel('Count')
    plt.legend(['Legit', 'Phishing'])
    plt.xticks(rotation=0)
    
    # 12. Feature correlation heatmap (selected features)
    plt.subplot(3, 4, 12)
    numeric_features = ['suspicious_word_count', 'urgency_score', 'exclamation_count', 
                       'caps_ratio', 'money_mentions', 'text_length', 'word_count']
    corr_matrix = df[numeric_features].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
    plt.title('Feature Correlation Matrix')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary statistics
    print("\n=== ENHANCED DATASET ANALYSIS ===")
    print(f"Total samples: {len(df)}")
    print(f"Phishing samples: {len(df[df['label'] == 'phishing'])}")
    print(f"Legitimate samples: {len(df[df['label'] == 'legit'])}")
    
    print("\n=== KEY FEATURE INSIGHTS ===")
    
    # Suspicious words analysis
    avg_suspicious_phishing = df[df['label'] == 'phishing']['suspicious_word_count'].mean()
    avg_suspicious_legit = df[df['label'] == 'legit']['suspicious_word_count'].mean()
    print(f"Average suspicious words - Phishing: {avg_suspicious_phishing:.2f}, Legit: {avg_suspicious_legit:.2f}")
    
    # Domain analysis
    suspicious_domains_phishing = df[(df['label'] == 'phishing') & (df['sender_domain_suspicious'])].shape[0]
    suspicious_domains_legit = df[(df['label'] == 'legit') & (df['sender_domain_suspicious'])].shape[0]
    print(f"Suspicious domains - Phishing: {suspicious_domains_phishing}, Legit: {suspicious_domains_legit}")
    
    # Authentication analysis
    failed_auth_phishing = df[(df['label'] == 'phishing') & (df['spfrecord'] == 'fail')].shape[0]
    failed_auth_legit = df[(df['label'] == 'legit') & (df['spfrecord'] == 'fail')].shape[0]
    print(f"Failed SPF - Phishing: {failed_auth_phishing}, Legit: {failed_auth_legit}")
    
    # Urgency analysis
    urgent_phishing = df[(df['label'] == 'phishing') & (df['urgency_score'] > 0)].shape[0]
    urgent_legit = df[(df['label'] == 'legit') & (df['urgency_score'] > 0)].shape[0]
    print(f"Urgent language - Phishing: {urgent_phishing}, Legit: {urgent_legit}")
    
    print("\n=== FEATURE QUALITY METRICS ===")
    
    # Calculate feature separability
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    feature_separability = {}
    
    for col in numeric_cols:
        if col != 'label':
            phishing_mean = df[df['label'] == 'phishing'][col].mean()
            legit_mean = df[df['label'] == 'legit'][col].mean()
            pooled_std = df[col].std()
            
            if pooled_std > 0:
                separability = abs(phishing_mean - legit_mean) / pooled_std
                feature_separability[col] = separability
    
    # Sort by separability
    sorted_features = sorted(feature_separability.items(), key=lambda x: x[1], reverse=True)
    
    print("Top 10 most separable features:")
    for i, (feature, sep) in enumerate(sorted_features[:10]):
        print(f"{i+1:2d}. {feature:<25} {sep:.3f}")
    
    return df

def create_feature_comparison():
    """Create a comparison between original and enhanced features"""
    
    original_features = [
        'label', 'text', 'urls', 'sender', 'spfrecord'
    ]
    
    enhanced_features = [
        'text_length', 'word_count', 'avg_words_per_sentence', 
        'suspicious_word_count', 'urgency_score', 'exclamation_count', 
        'caps_ratio', 'money_mentions', 'personal_info_requests',
        'sender_domain_suspicious', 'sender_tld', 'sender_domain_length', 
        'sender_domain_spoofed', 'url_count', 'suspicious_url', 
        'url_shortener', 'url_ip_address', 'url_suspicious_tld',
        'timestamp', 'day_of_week', 'hour_sent', 'email_client', 
        'dkim_valid', 'dmarc_pass', 'priority', 'message_size_bytes'
    ]
    
    print("=== DATASET ENHANCEMENT SUMMARY ===")
    print(f"Original features: {len(original_features)}")
    print(f"Enhanced features: {len(enhanced_features)}")
    print(f"Total features: {len(original_features) + len(enhanced_features)}")
    print(f"Improvement: {((len(enhanced_features) + len(original_features)) / len(original_features) - 1) * 100:.0f}% more features")
    
    # Feature categories
    categories = {
        'Text Analysis': ['text_length', 'word_count', 'avg_words_per_sentence', 
                         'suspicious_word_count', 'urgency_score', 'exclamation_count', 
                         'caps_ratio', 'money_mentions', 'personal_info_requests'],
        'Sender Analysis': ['sender_domain_suspicious', 'sender_tld', 'sender_domain_length', 
                           'sender_domain_spoofed'],
        'URL Analysis': ['url_count', 'suspicious_url', 'url_shortener', 
                        'url_ip_address', 'url_suspicious_tld'],
        'Email Metadata': ['timestamp', 'day_of_week', 'hour_sent', 'email_client', 
                          'dkim_valid', 'dmarc_pass', 'priority', 'message_size_bytes']
    }
    
    print(f"\nFeature Categories:")
    for category, features in categories.items():
        print(f"  {category}: {len(features)} features")

if __name__ == "__main__":
    # Analyze the enhanced dataset
    df = analyze_enhanced_dataset("data/emails_train_enhanced.csv")
    
    # Show feature comparison
    create_feature_comparison()
    
    print("\n✅ Analysis complete! Check 'dataset_analysis.png' for visualizations.")
