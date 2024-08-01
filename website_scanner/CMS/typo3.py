import re
import requests
from website_scanner.path_checker import check_path


class Typo3:
    def __init__(self, response_text, headers, url):
        self.response_text = response_text
        self.headers = headers
        self.url = url
        self.cms = 'Typo3'
        self.version = 'Not detected'

    def detect(self):
        if 'typo3' in self.response_text.lower():
            version = re.search(r'typo3 (\d+\.\d+(\.\d+)?)', self.response_text, re.IGNORECASE)
            if version:
                self.version = version.group(1)
            return self.cms, self.version

        if 'x-generator' in self.headers and 'typo3' in self.headers['x-generator'].lower():
            return self.cms, self.version

        generator_meta = re.search(r'<meta name="generator" content="TYPO3 (\d+\.\d+(\.\d+)?)"', self.response_text)
        if generator_meta:
            self.version = generator_meta.group(1)
            return self.cms, self.version

        return None, None

    def check_typo3_scripts(self):
        scripts = re.findall(r'/typo3conf/ext/([^/]+)/', self.response_text)
        return scripts if scripts else None

    def get_template(self):
        templates = re.findall(r'/typo3conf/ext/([^/]+)/Resources/', self.response_text)
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
        if re.search(r'This website is powered by TYPO3', self.response_text, re.IGNORECASE):
            return True
        return False

    def get_info(self):
        info = {
            'cms': self.cms,
            'version': self.version,
            'template': self.get_template(),
            'scripts': self.check_typo3_scripts(),
            'security_headers': self.check_security_headers(),
            'content_string': self.check_content_string()
        }
        return info
    
def check_typo3_paths(domain, headers, cookies):
    typo3_paths = [
        'typo3/', 'typo3conf/', 'typo3temp/', 'typo3_src/', 
        'uploads/', 'fileadmin/', 'typo3_src/', 'tslib/', 'typo3/sysext/'
    ]
    for path in typo3_paths:
        check_path(domain, path, headers, cookies)
