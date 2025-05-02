import re
import math
import tldextract
import requests
import pandas as pd
from urllib.parse import urlparse

# Đọc domain phổ biến từ file
trusted_df = pd.read_csv('top-1m.csv', header=None)
TRUSTED_DOMAINS = set(trusted_df[0].str.strip().str.lower())

# Đọc tld đáng ngờ từ file
tld_df = pd.read_csv('suspicious_tld.csv', header=None)
SUSPICIOUS_TLDS = set(tld_df[0].str.strip().str.lower())

# Hàm tính entropy
def shannon_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in set(data):
        p = data.count(x) / len(data)
        entropy -= p * math.log2(p)
    return entropy

# Hàm check https    
def has_https(domain, timeout=5):
    try:
        response = requests.get(f"https://{domain}", timeout=timeout)
        return response.status_code < 400  # Status code < 400 coi như hợp lệ
    except requests.exceptions.SSLError:
        return False
    except requests.exceptions.RequestException:
        return False

# Hàm phân loại dữ liệu
def extract_features(url):
    parsed = urlparse(url)
    ext = tldextract.extract(url)

    domain = ext.domain + "." + ext.suffix
    subdomain = ext.subdomain
    full_domain = '.'.join([subdomain, ext.domain, ext.suffix]) if subdomain else domain

    features = {}

    features['url_length'] = len(url)
    features['has_https'] = has_https(domain)
    features['count_dot'] = url.count('.')
    features['count_hyphen'] = url.count('-')
    features['count_special_characters'] = len(re.findall(r'[^\w\s]', url))
    features['has_login_keyword'] = 1 if re.search(r'login|verify|update|secure|account|bank', url, re.IGNORECASE) else 0
    features['domain_length'] = len(domain)
    features['count_digits_in_domain'] = sum(c.isdigit() for c in domain)
    features['domain_entropy'] = shannon_entropy(domain)
    features['subdomain_length'] = len(subdomain)
    features['count_subdomains'] = subdomain.count('.') + 1 if subdomain else 0
    features['url_path_length'] = len(parsed.path)
    features['is_ip'] = int(bool(re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed.hostname or "")))
    features['trusted_domain'] = int(domain in TRUSTED_DOMAINS)
    features['tld_is_suspicious'] = int(ext.suffix.lower() in SUSPICIOUS_TLDS)

    return features

