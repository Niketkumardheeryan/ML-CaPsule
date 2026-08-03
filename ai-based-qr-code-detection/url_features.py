import re
import urllib.parse


SUSPICIOUS_TERMS = [
    'login', 'secure', 'verify', 'update', 'bank', 'account', 'confirm', 'signin', 'webscr', 'ebayisapi',
    'paypal', 'update', 'support', 'wallet', 'transaction', 'secure-login', 'confirm', 'verify-now',
]


def extract_url_features(url):
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parsed.query.lower()
    full_url = url.lower()

    features = {
        'url_length': len(full_url),
        'domain_length': len(domain),
        'path_length': len(path),
        'has_query': 1 if query else 0,
        'num_dots': domain.count('.') + path.count('.'),
        'num_hyphens': full_url.count('-'),
        'num_at': full_url.count('@'),
        'num_percent': full_url.count('%'),
        'num_equals': full_url.count('='),
        'num_slashes': full_url.count('/'),
        'is_ip_address': int(is_ip_address(domain)),
        'suspicious_term_count': suspicious_term_count(full_url),
    }

    return features


def is_ip_address(domain):
    return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain))


def suspicious_term_count(text):
    return sum(1 for term in SUSPICIOUS_TERMS if term in text)
