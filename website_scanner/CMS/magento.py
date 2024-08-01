import re
import requests
from website_scanner.path_checker import check_path

class Magento:
    def __init__(self, response_text, headers, url):
        self.response_text = response_text
        self.headers = headers
        self.url = url
        self.cms = 'Magento'
        self.version = 'Not detected'

    def detect(self):
        if 'mage-' in self.response_text.lower() or 'magento' in self.response_text.lower():
            version = re.search(r'magento (\d+\.\d+(\.\d+)?)', self.response_text, re.IGNORECASE)
            if version:
                self.version = version.group(1)
            return self.cms, self.version

        if 'x-magento-init' in self.headers:
            return self.cms, self.version

        generator_meta = re.search(r'<meta name="generator" content="Magento (\d+\.\d+(\.\d+)?)"', self.response_text)
        if generator_meta:
            self.version = generator_meta.group(1)
            return self.cms, self.version

        return None, None

    def check_magento_scripts(self):
        scripts = re.findall(r'/pub/static/([^/]+)/', self.response_text)
        return scripts if scripts else None

    def get_template(self):
        templates = re.findall(r'/pub/static/frontend/([^/]+)/', self.response_text)
        if templates:
            return templates[0]
        return None

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
        if re.search(r'This website is powered by Magento', self.response_text, re.IGNORECASE):
            return True
        return False

    def get_info(self):
        info = {
            'cms': self.cms,
            'version': self.version,
            'template': self.get_template(),
            'scripts': self.check_magento_scripts(),
            'security_headers': self.check_security_headers(),
            'content_string': self.check_content_string()
        }
        return info
    
def check_magento_paths(domain, headers, cookies):
    magento_paths = [
        'pub/static/', 'var/log/', 'app/etc/', 'vendor/',
        'pub/media/', 'app/code/', 'setup/', 'bin/', 'dev/', 
        'lib/', 'phpserver/', 'var/cache/', 'var/page_cache/'
    ]
    for path in magento_paths:
        check_path(domain, path, headers, cookies)
