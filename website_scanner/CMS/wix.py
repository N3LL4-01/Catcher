import re
import requests
from website_scanner.path_checker import check_path

class Wix:
    def __init__(self, response_text, headers, url):
        self.response_text = response_text
        self.headers = headers
        self.url = url
        self.cms = 'Wix'
        self.version = 'Not detected'

    def detect(self):
        if 'wix' in self.response_text.lower() or 'x-wix' in self.headers:
            return self.cms, self.version

        if re.search(r'wix.com', self.response_text, re.IGNORECASE):
            return self.cms, self.version

        generator_meta = re.search(r'<meta name="generator" content="Wix.com Website Builder"', self.response_text)
        if generator_meta:
            return self.cms, self.version

        return None, None

    def check_wix_scripts(self):
        scripts = re.findall(r'wixcode-platform', self.response_text, re.IGNORECASE)
        return scripts if scripts else None

    def check_security_headers(self):
        security_headers = {
            'Strict-Transport-Security': self.headers.get('Strict-Transport-Security'),
            'Content-Security-Policy': self.headers.get('Content-Security-Policy'),
            'X-Content-Type-Options': self.headers.get('X-Content-Type-Options'),
            'X-Frame-Options': self.headers.get('X-Frame-Options'),
            'X-XSS-Protection': self.headers.get('X-XSS-Protection')
        }
        return security_headers

    def check_content_string(self):
        if re.search(r'wixstatic.com', self.response_text, re.IGNORECASE):
            return True
        return False

    def get_info(self):
        info = {
            'cms': self.cms,
            'version': self.version,
            'scripts': self.check_wix_scripts(),
            'security_headers': self.check_security_headers(),
            'content_string': self.check_content_string()
        }
        return info
    
def check_wix_paths(domain, headers, cookies):
    wix_paths = [
        'images/', 'uploads/', 'files/', 'static/', 'media/'
    ]
    for path in wix_paths:
        check_path(domain, path, headers, cookies)
