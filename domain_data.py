import pandas as pd
import json

def load_data():
    df = pd.read_csv('domain_data3.csv')
    
    data = []
    for _, row in df.iterrows():
        whois_info = json.loads(row['whois_info'])  # Convert JSON string back to dictionary
        web_content = row['web_content']
        ssl_info = json.loads(row['ssl_info'])  # Convert JSON string back to dictionary
        data.append({
            'domain': row['domain'],
            'whois_info': whois_info,
            'web_content': web_content,
            'ssl_info': ssl_info
        })
    
    return data

def main():
    data = load_data()
    for entry in data:
        print(f"Domain: {entry['domain']}")
        print(f"WHOIS Info: {entry['whois_info']}")
        print(f"SSL Info: {entry['ssl_info']}")
        # Additional processing can be done here

if __name__ == "__main__":
    main()
