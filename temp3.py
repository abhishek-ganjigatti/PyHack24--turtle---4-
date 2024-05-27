import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import json

def load_data():
    df = pd.read_csv('domain_data5.csv')
    
    data = []
    for _, row in df.iterrows():
        whois_info = json.loads(row['whois_info'])  # Convert JSON string back to dictionary
        web_content = row['web_content']
        ssl_info = json.loads(row['ssl_info'])  # Convert JSON string back to dictionary
        data.append({
            'whois_info': whois_info,
            'web_content': web_content,
            'ssl_info': ssl_info
        })
    
    # Example labels - you need to replace this with actual labels
    labels = [0, 1, 0, 1]  # Example: 0 for legitimate, 1 for phishing
    return pd.DataFrame(data), labels

def extract_features(df):
    # Example feature extraction from domain data
    # Replace this with your actual feature extraction code
    whois_features = df['whois_info'].apply(lambda x: len(x))
    web_content_features = df['web_content'].apply(lambda x: len(x))
    
    features_df = pd.DataFrame({
        'whois_features': whois_features,
        'web_content_features': web_content_features
    })
    
    return features_df

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    return clf

def main():
    # Load data
    data, labels = load_data()
    
    # Extract features
    X = extract_features(data)
    y = labels  # Assuming labels are provided separately
    
    # Train the model
    model = train_model(X, y)
    
    # Save the trained model
    joblib.dump(model, 'phishing_detector1.pkl')

if __name__ == "__main__":
    main()
