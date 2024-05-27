import streamlit as st
import requests
from bs4 import BeautifulSoup
import whois
import joblib
import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
import time

def get_web_content(domain):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    urls = [f"http://{domain}", f"https://{domain}"]
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.prettify()
        except requests.HTTPError as e:
            st.error(f"Failed to fetch content for {url}: {e}")
        except requests.RequestException as e:
            st.error(f"Request exception for {url}: {e}")
    return None

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        st.error(f"WHOIS lookup failed for {domain}: {e}")
        return None

def extract_features(whois_info, web_content):
    # Example feature extraction from domain data
    # Replace this with your actual feature extraction code
    whois_features = len(whois_info) if whois_info else 0
    web_content_features = len(web_content) if web_content else 0
    
    features_df = pd.DataFrame({
        'whois_features': [whois_features],
        'web_content_features': [web_content_features]
    })
    
    return features_df

def load_model():
    return joblib.load('phishing_detector1.pkl')

def main():
    st.title("Website Safety Checker")

    domain = st.text_input("Enter the domain name (e.g., example.com):")

    if st.button("Check Website Safety"):
        if not domain:
            st.warning("Please enter a domain name.")
        else:
            start_time = time.time()  # Start time for processing

            st.info(f"Fetching data for {domain}...")

            web_content = get_web_content(domain)
            whois_info = get_whois_info(domain)

            if web_content and whois_info:
                # Load existing data to compare source code
                existing_data = pd.read_csv('domain_source_code_f.csv')
                
                match_found = any(existing_data['web_content'] == web_content)
                if match_found:
                    st.info("Website source code matches with our database.")
                else:
                    st.warning("Website source code does not match our database.")
                
                st.info("Running the ML model to check safety...")
                features = extract_features(json.dumps(whois_info, default=str), web_content)
                model = load_model()
                prediction = model.predict(features)[0]

                if prediction == 1:
                    st.error("The website is potentially unsafe (phishing).")
                else:
                    st.success("The website appears to be safe.")

                end_time = time.time()  # End time for processing
                processing_time = end_time - start_time
                st.info(f"Processing time: {processing_time:.2f} seconds")
            else:
                st.error("Failed to fetch necessary information for the domain.")

if __name__ == "__main__":
    main()
