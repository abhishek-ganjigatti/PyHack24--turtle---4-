import streamlit as st
import requests
from bs4 import BeautifulSoup
import whois
import joblib
import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier

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

    domain = st.text_input("Enter the domain name (e.g., example.com):").strip()

    if st.button("Check Website Safety"):
        if not domain:
            st.warning("Please enter a domain name.")
        else:
            st.info(f"Fetching data for {domain}...")

            # Check if the domain already exists in the CSV file
            try:
                existing_data = pd.read_csv('websites.csv')
            except FileNotFoundError:
                st.error("The CSV file 'websites.csv' was not found.")
                return

            if domain in existing_data['Website'].values:
                st.info("Website is safe to proceed.")
                web_content = None
            else:
                st.warning("Domain not found in the database. Fetching new data...")
                if domain.startswith("http://") or domain.startswith("https://"):
                    domain = domain.split("://")[1]

                web_content = get_web_content(domain)
                whois_info = get_whois_info(domain)

                if web_content and whois_info:
                    st.info("Running the ML model to check safety...")
                    features = extract_features(json.dumps(whois_info, default=str), web_content)
                    model = load_model()
                    prediction = model.predict(features)[0]

                    if prediction == 1:
                        st.error("The website is potentially unsafe (phishing).")
                    else:
                        st.success("The website appears to be safe.")
                else:
                    st.error("Failed to fetch necessary information for the domain.")

if __name__ == "__main__":
    main()
