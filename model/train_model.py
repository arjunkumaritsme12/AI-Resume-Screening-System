"""
Train machine learning model for resume classification.
Classifies resumes into predefined job categories.
"""

import pandas as pd
import numpy as np
import re
import pickle
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "model"

# Create models directory if it doesn't exist
MODEL_DIR.mkdir(exist_ok=True)


def cleanResume(txt):
    """Clean and normalize resume text."""
    if not txt or not isinstance(txt, str):
        return ""
    
    txt = re.sub('http\\S+\\s*', ' ', txt)
    txt = re.sub('[^a-zA-Z ]', ' ', txt)
    txt = re.sub('\\s+', ' ', txt)
    return txt.lower().strip()


def load_data(csv_path):
    """Load and preprocess training data."""
    try:
        print(f"Loading data from: {csv_path}")
        df = pd.read_csv(csv_path)
        
        print(f"Loaded {len(df)} resumes")
        print(f"Categories: {df['Category'].unique()}")
        
        # Clean resumes
        print("Cleaning resumes...")
        df['Resume'] = df['Resume'].apply(cleanResume)
        
        # Remove empty resumes
        df = df[df['Resume'].str.len() > 100]
        print(f"After cleaning: {len(df)} valid resumes")
        
        return df
    except FileNotFoundError:
        print(f"Error: File not found: {csv_path}")
        return None
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None


def train_model(df):
    """Train classification model."""
    if df is None or len(df) == 0:
        print("No data available for training")
        return None, None, None
    
    print("\\n" + "="*50)
    print("TRAINING MODEL")
    print("="*50)
    
    # Features and labels
    X = df['Resume'].values
    y = df['Category'].values
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # TF-IDF Vectorization
    print("\\nVectorizing text...")
    tfidf = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )
    
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    print(f"TF-IDF features: {X_train_tfidf.shape[1]}")
    
    # Label encoding
    print("\\nEncoding labels...")
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)
    y_test_encoded = le.transform(y_test)
    
    print(f"Classes: {le.classes_}")
    
    # Train classifier
    print("\\nTraining SVM classifier...")
    model = LinearSVC(max_iter=5000, random_state=42, verbose=1)
    model.fit(X_train_tfidf, y_train_encoded)
    
    # Evaluate
    print("\\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test_encoded, y_pred)
    
    print(f"\\nAccuracy: {accuracy:.4f}")
    print("\\nClassification Report:")
    print(classification_report(y_test_encoded, y_pred, target_names=le.classes_))
    
    return model, tfidf, le, accuracy


def save_model(model, tfidf, le, model_dir=MODEL_DIR):
    """Save trained model and vectorizer."""
    try:
        print("\\n" + "="*50)
        print("SAVING MODEL")
        print("="*50)
        
        model_dir = Path(model_dir)
        model_dir.mkdir(exist_ok=True)
        
        # Save model
        model_path = model_dir / "classifier.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        print(f"✓ Model saved: {model_path}")
        
        # Save vectorizer
        tfidf_path = model_dir / "tfidf_vectorizer.pkl"
        with open(tfidf_path, "wb") as f:
            pickle.dump(tfidf, f)
        print(f"✓ Vectorizer saved: {tfidf_path}")
        
        # Save label encoder
        le_path = model_dir / "label_encoder.pkl"
        with open(le_path, "wb") as f:
            pickle.dump(le, f)
        print(f"✓ Label encoder saved: {le_path}")
        
        print("\\nModel training and saving completed successfully!")
        return True
    except Exception as e:
        print(f"Error saving model: {str(e)}")
        return False


def main():
    """Main training pipeline."""
    # Load data
    csv_path = DATA_DIR / "resumes.csv"
    df = load_data(csv_path)
    
    if df is None or len(df) == 0:
        print("\\nCannot proceed without data")
        return False
    
    # Train model
    model, tfidf, le, accuracy = train_model(df)
    
    if model is None:
        print("\\nModel training failed")
        return False
    
    # Save model
    success = save_model(model, tfidf, le)
    
    return success


if __name__ == "__main__":
    import sys
    
    print("Resume Classification Model Training")
    print("="*50)
    
    success = main()
    
    if success:
        print("\\n✓ Training pipeline completed successfully!")
        sys.exit(0)
    else:
        print("\\n✗ Training pipeline failed")
        sys.exit(1)
