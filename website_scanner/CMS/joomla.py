import re
import requests
from website_scanner.path_checker import check_path


class Joomla:
    def __init__(self, response_text, headers, url):
        self.response_text = response_text
        self.headers = headers
        self.url = url
        self.cms = 'Joomla'
        self.version = 'Not detected'

    def detect(self):
        if 'joomla' in self.response_text.lower():
            version = re.search(r'joomla (\d+\.\d+(\.\d+)?)', self.response_text, re.IGNORECASE)
            if version:
                self.version = version.group(1)
            return self.cms, self.version

        if 'x-generator' in self.headers and 'joomla' in self.headers['x-generator'].lower():
            return self.cms, self.version

        generator_meta = re.search(r'<meta name="generator" content="Joomla! (\d+\.\d+(\.\d+)?)"', self.response_text)
        if generator_meta:
            self.version = generator_meta.group(1)
            return self.cms, self.version

        return None, None

    def check_readme(self):
        response = requests.get(f"{self.url}/README.txt", headers=self.headers)
        if response.status_code == 200 and "2- What is Joomla?" in response.text:
            return True
        return False

    def check_template_details(self):
        response = requests.get(f"{self.url}/templates/protostar/templateDetails.xml", headers=self.headers)
        if response.status_code == 200 and re.search(r'<!DOCTYPE install PUBLIC "-//Joomla!', response.text):
            return True
        return False

    def check_core_js(self):
        response = requests.get(f"{self.url}/media/system/js/core.js", headers=self.headers)
        if response.status_code == 200 and "var Joomla={};" in response.text.splitlines()[3]:
            return True
        return False

    def check_core_site_js(self):
        response = requests.get(f"{self.url}/site/media/system/js/core.js", headers=self.headers)
        if response.status_code == 200 and re.search(r'^Joomla=window\.Joomla', response.text):
            return True
        return False

    def get_template(self):
        templates = re.findall(r'/templates/([^/]+)/css/template\.css', self.response_text)
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

    def get_info(self):
        info = {
            'cms': self.cms,
            'version': self.version,
            'readme_exists': self.check_readme(),
            'template_details_exists': self.check_template_details(),
            'core_js_exists': self.check_core_js(),
            'core_site_js_exists': self.check_core_site_js(),
            'template': self.get_template(),
            'security_headers': self.check_security_headers()
        }
        return info
    
def check_joomla_paths(domain, headers, cookies):
    joomla_paths = [
        'administrator/', 'components/', 'images/', 'includes/',
        'language/', 'libraries/', 'media/', 'modules/',
        'plugins/', 'templates/', 'cache/', 'cli/', 'logs/', 
        'tmp/', 'xmlrpc/'
    ]
    for path in joomla_paths:
        check_path(domain, path, headers, cookies)
