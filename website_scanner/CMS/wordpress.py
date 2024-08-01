import re
import requests
from website_scanner.path_checker import check_path

import re
import requests

class WordPress:
    def __init__(self, response_text, headers, url):
        self.response_text = response_text
        self.headers = headers
        self.url = url
        self.cms = 'WordPress'
        self.version = 'Not detected'

    def detect(self):
        if 'wp-content' in self.response_text or 'wp-includes' in self.response_text:
            version = re.search(r'wordpress (\d+\.\d+(\.\d+)?)', self.response_text)
            if version:
                self.version = version.group(1)
            return self.cms, self.version

        if 'x-powered-by' in self.headers and 'wordpress' in self.headers['x-powered-by'].lower():
            return self.cms, self.version

        generator_meta = re.search(r'<meta name="generator" content="WordPress (\d+\.\d+(\.\d+)?)"', self.response_text)
        if generator_meta:
            self.version = generator_meta.group(1)
            return self.cms, self.version

        return None, None

    def get_template(self):
        templates = re.findall(r'/wp-content/themes/([^/]+)/', self.response_text)
        if templates:
            return templates[0]
        return None

    def check_plugins(self):
        plugins = re.findall(r'/wp-content/plugins/([^/]+)/', self.response_text)
        return list(set(plugins))  # Remove duplicates

    def check_security_headers(self):
        security_headers = {
            'Strict-Transport-Security': self.headers.get('Strict-Transport-Security'),
            'Content-Security-Policy': self.headers.get('Content-Security-Policy'),
            'X-Content-Type-Options': self.headers.get('X-Content-Type-Options'),
            'X-Frame-Options': self.headers.get('X-Frame-Options'),
            'X-XSS-Protection': self.headers.get('X-XSS-Protection')
        }
        return security_headers

    def check_file_upload_vulnerability(self):
        response = requests.get(f"{self.url}/wp-content/uploads/", headers=self.headers)
        if response.status_code == 200 and "Index of" in response.text:
            return True
        return False

    def get_info(self):
        info = {
            'cms': self.cms,
            'version': self.version,
            'template': self.get_template(),
            'plugins': self.check_plugins(),
            'security_headers': self.check_security_headers(),
            'file_upload_vulnerability': self.check_file_upload_vulnerability()
        }
        return info

def check_wordpress_paths(domain, headers, cookies):
    wp_paths = [
        'wp-includes/', 'wp-includes/images/', 'wp-content/',
        'wp-content/uploads/', 'wp-content/themes/', 'wp-content/plugins/',
        'wp-content/plugins/hustle/views/admin/dashboard/', 'wp-admin/',
        'wp-cron.php', 'readme.html', 'xmlrpc.php'
    ]
    for path in wp_paths:
        check_path(domain, path, headers, cookies)
