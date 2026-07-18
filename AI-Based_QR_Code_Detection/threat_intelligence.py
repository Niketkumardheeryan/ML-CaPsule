import requests
import urllib.parse


class ThreatIntelligence:
    def __init__(self):
        self.virustotal_api_key = None
        self.abuseipdb_api_key = None

    def set_virustotal_key(self, api_key):
        self.virustotal_api_key = api_key

    def set_abuseipdb_key(self, api_key):
        self.abuseipdb_api_key = api_key

    def check_virustotal(self, url):
        if not self.virustotal_api_key:
            return {'status': 'api_key_not_set', 'malicious_count': 0}

        try:
            params = {
                'apikey': self.virustotal_api_key,
                'resource': url,
            }
            response = requests.get('https://www.virustotal.com/api/v2/url/report', params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'success',
                    'malicious_count': data.get('positives', 0),
                    'total_scanners': data.get('total', 0),
                    'report_url': data.get('permalink', '')
                }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

        return {'status': 'not_found'}

    def check_abuseipdb(self, domain):
        if not self.abuseipdb_api_key:
            return {'status': 'api_key_not_set', 'abuse_confidence_score': 0}

        try:
            headers = {
                'Key': self.abuseipdb_api_key,
                'Accept': 'application/json'
            }
            params = {'domain': domain}
            response = requests.get('https://api.abuseipdb.com/api/v2/domain-check', headers=headers, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'success',
                    'abuse_confidence_score': data.get('data', {}).get('abuseConfidenceScore', 0),
                    'total_reports': data.get('data', {}).get('totalReports', 0)
                }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

        return {'status': 'not_found'}

    def is_recently_registered(self, domain):
        '''Check if domain appears suspicious based on patterns (basic check)'''
        suspicious_domains = ['bit.ly', 'tinyurl.com', 'short.link', 'ow.ly', 'bit.cc']
        for pattern in suspicious_domains:
            if pattern in domain:
                return True
        return False
