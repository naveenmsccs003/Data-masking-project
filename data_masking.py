import re
import pandas as pd

df = pd.read_excel('chatbottestingdatas.xlsx')
data = pd.DataFrame(df)
data['Entry']
patterns = {
    'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
    'phone_number': r'(\b\d{10}\b)',
    'api_key': r'(?i)api\s*[:=]?\s*([a-zA-Z0-9-_]{8,})'
}

def calculate_risk(row):
    score = 0
    if pd.notna(row['email']): score += 1
    if pd.notna(row['phone_number']): score += 3
    if pd.notna(row['api_key']): score += 5
    return score

for col, regex in patterns.items():
    data[col] = data['Entry'].str.extract(regex)

data['risk_score'] = data.apply(calculate_risk, axis=1)   

def mask_text_content(text):
    if pd.isna(text) or not isinstance(text, str):
        return text
    # Mask Email: 
    text = re.sub(r'([a-zA-Z0-9._%+-])[a-zA-Z0-9._%+-]*@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'\1*****@\2', text)
    # Mask Phone: 
    text = re.sub(r'\b(\d)\d{7}(\d{2})\b', r'\1*******\2', text)
    # Mask API Key:
    text = re.sub(r'(?i)(api\s*[:=]?\s*[a-zA-Z0-9]{4})[a-zA-Z0-9_-]+', r'\1****************', text)
    return text
    
data['Entry'] = data['Entry'].apply(mask_text_content)
