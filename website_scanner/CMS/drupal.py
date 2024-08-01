import re
import requests
from website_scanner.path_checker import check_path


class Drupal:
    def __init__(self, response_text, headers, url):
        self.response_text = response_text
        self.headers = headers
        self.url = url
        self.cms = 'Drupal'
        self.version = 'Not detected'

    def detect(self):
        if 'sites/all' in self.response_text or 'drupal' in self.response_text.lower():
            version = re.search(r'drupal (\d+\.\d+(\.\d+)?)', self.response_text)
            if version:
                self.version = version.group(1)
            return self.cms, self.version

        if 'x-generator' in self.headers and 'drupal' in self.headers['x-generator'].lower():
            return self.cms, self.version

        generator_meta = re.search(r'<meta name="generator" content="Drupal (\d+\.\d+(\.\d+)?)"', self.response_text)
        if generator_meta:
            self.version = generator_meta.group(1)
            return self.cms, self.version

        return None, None

    def check_readme(self):
        response = requests.get(f"{self.url}/sites/all/README.txt", headers=self.headers)
        if response.status_code == 200 and "Drupal" in response.text:
            return True
        return False

    def check_changelog(self):
        response = requests.get(f"{self.url}/CHANGELOG.txt", headers=self.headers)
        if response.status_code == 200 and "Drupal" in response.text.splitlines()[1]:
            return True
        return False

    def check_changelog_d8(self):
        response = requests.get(f"{self.url}/core/CHANGELOG.txt", headers=self.headers)
        if response.status_code == 200 and "Drupal" in response.text.splitlines()[0]:
            return True
        return False

    def check_node_css(self):
        response = requests.get(f"{self.url}/modules/node/node.css", headers=self.headers)
        if response.status_code == 200 and ".node-" in response.text.splitlines()[1]:
            return True
        return False

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
            'changelog_exists': self.check_changelog(),
            'changelog_d8_exists': self.check_changelog_d8(),
            'node_css_exists': self.check_node_css(),
            'security_headers': self.check_security_headers()
        }
        return info
    
def check_drupal_paths(domain, headers, cookies):
    drupal_paths = [
        'core/', 'modules/', 'profiles/', 'sites/',
        'themes/', 'includes/', 'misc/', 'scripts/',
        'web.config', 'robots.txt'
    ]
    for path in drupal_paths:
        check_path(domain, path, headers, cookies)
