import socket
import ssl
import re
import requests
import platform
import sys
import os
import dns.resolver
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from colorama import Fore, Style, init
from bs4 import BeautifulSoup
import urllib3
from website_scanner.CMS.wix import Wix
from website_scanner.CMS.wordpress import WordPress
from website_scanner.CMS.drupal import Drupal
from website_scanner.CMS.joomla import Joomla
from website_scanner.CMS.typo3 import Typo3
from website_scanner.CMS.magento import Magento
from website_scanner.path_checker import check_path


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


init(autoreset=True)

fg = Fore.GREEN
fr = Fore.RED
fw = Fore.WHITE
fy = Fore.YELLOW
fo = Fore.LIGHTYELLOW_EX
flc = Fore.CYAN
bd = Style.BRIGHT
res = Style.RESET_ALL


def print_logo():
    logo_magenta = Fore.MAGENTA
    logo_cyan = Fore.CYAN
    reset = Style.RESET_ALL

    logo = [
        "⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿",
        "⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿",
        "⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿",
        "⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿  ███████████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗",
        "⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿██╔════██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗",
        "⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿██║    ███████║   ██║   ██║     ███████║█████╗  ██████╔╝",
        "⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿██║    ██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗",
        "⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿╚██████╗██║  ██║   ██║   ╚██████╗██║  ██║███████╗██║  ██║",
        "⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═╝  ╚═╝",
        "⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿",
        "⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿" @n3ll4 v0.1,
    ]

    for line in logo:
        colored_line = ""
        for char in line:
            if char == '█':
                colored_line += logo_magenta + char
            elif char == '▓' or char == '⢿':
                colored_line += logo_magenta + char
            elif char == '▒' or char == '░' or char == '⡏' or char == '⣿' or char == '⣧' or char == '⠏':
                colored_line += logo_cyan + char
            else:
                colored_line += reset + char
        print(colored_line + reset)

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.error as e:
        print(f"{fr}[-] Error getting IP address: {e}{fw}")
        return None

def get_cookies(domain):
    os_type = platform.system()
    if os_type == "Windows":
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver.exe')
    elif os_type in ["Linux", "Darwin"]:  
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver')
    else:
        raise Exception(f"Unsupported OS: {os_type}")
        
    service = FirefoxService(executable_path=geckodriver_path)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(service=service, options=options)

    cookies = {}
    try:
        driver.get(domain)
        for cookie in driver.get_cookies():
            cookie_name = cookie['name']
            cookies[cookie_name] = cookie['value']
            is_httponly = cookie.get('httpOnly', False)
            is_secure = cookie.get('secure', False)
            samesite = cookie.get('sameSite', 'None')

            print(f"{fg}[+] Cookie: {cookie_name}{fw}")
            if is_httponly:
                print(f"    {fg}HttpOnly: {is_httponly}{fw}")
            else:
                print(f"    {fr}HttpOnly: {is_httponly} - Vulnerable{fw}")

            if is_secure:
                print(f"    {fg}Secure: {is_secure}{fw}")
            else:
                print(f"    {fr}Secure: {is_secure} - Vulnerable{fw}")

            print(f"    SameSite: {samesite}")

    except Exception as e:
        print(f"{fr}[-] Error collecting cookies: {e}{fw}")
    finally:
        driver.quit()
    
    return cookies

def detect_cms(response, url):
    cms_detectors = [
        WordPress,
        Joomla,
        Drupal,
        Typo3,
        Magento,
        Wix
    ]

    for detector_class in cms_detectors:
        detector = detector_class(response.text, response.headers, url)
        cms, version = detector.detect()
        if cms:
            return cms, version, detector.get_info()

    return "Unknown", "Not detected", {}

def get_php_version(headers):
    php_version = "Unknown"
    if 'x-powered-by' in headers:
        php_header = headers['x-powered-by'].lower()
        match = re.search(r'php\/(\d+\.\d+(\.\d+)?)', php_header)
        if match:
            php_version = match.group(1)
    return php_version

def get_webserver_info(headers):
    try:
        server = headers.get('Server', 'Unknown')
        x_powered_by = headers.get('X-Powered-By', 'Unknown')
        if isinstance(server, list):
            server = server[0]
        return server, x_powered_by
    except Exception as e:
        print(f"Could not detect web server information: {e}")
        return 'Unknown', 'Unknown'

def get_os_info(response):
    server = response.headers.get('Server', 'Unknown')
    os_info = 'Unknown'
    if 'nginx' in server.lower():
        os_info = 'Nginx'
    elif 'apache' in server.lower():
        os_info = 'Apache'
    elif 'iis' in server.lower():
        os_info = 'IIS'
    return os_info

def mx_lookup(site):
    try:
        mx_records = dns.resolver.resolve(site, 'MX')
        if not mx_records:
            print(f"{Fore.RED}[-] No MX records found for {site}{Fore.WHITE}")
            return

        mx_record = mx_records[0].exchange.to_text()
        mx_ip = socket.gethostbyname(mx_record)
        mx_hostname = socket.gethostbyaddr(mx_ip)[0]
        mx_result = f"{Fore.GREEN}IP      :{Fore.GREEN} {mx_ip}\n{Fore.GREEN}HOSTNAME:{Fore.WHITE} {mx_hostname}{Fore.WHITE}"
        print(f"{Fore.GREEN}[+] MX Lookup for{Fore.WHITE} {site}")

        print(mx_result)
    except dns.resolver.NoAnswer:
        print(f"{Fore.RED}[-] Error: The DNS response does not contain an answer to the question: {site}. IN MX{Fore.WHITE}")
    except dns.resolver.NXDOMAIN:
        print(f"{Fore.RED}[-] Error: The domain {site} does not exist{Fore.WHITE}")
    except dns.resolver.Timeout:
        print(f"{Fore.RED}[-] Error: Timeout while resolving MX records for {site}{Fore.WHITE}")
    except dns.exception.DNSException as e:
        print(f"{Fore.RED}[-] DNS error: {e}{Fore.WHITE}")
    except socket.gaierror as e:
        print(f"{Fore.RED}[-] Error getting IP address for MX record: {e}{Fore.WHITE}")
    except Exception as e:
        print(f"{Fore.RED}[-] Unexpected error: {e}{Fore.WHITE}")

import requests

def scrape_wordpress_users(domain):
    # Fetch users from REST API
    users_url = domain + "/wp-json/wp/v2/users/"
    try:
        response = requests.get(users_url, verify=False)
        if response.status_code == 200:
            users = response.json()
            if users:
                print(f"\n{fg}[+] WordPress Users (from REST API):{fw}")
                for user in users:
                    print(f"  - {user['name']} ({user['slug']})")
            else:
                print(f"{fr}[-] No WordPress users found.{fw}")
        else:
            print(f"{fr}[-] Error fetching WordPress users: Status code {response.status_code}{fw}")
    except requests.exceptions.RequestException as e:
        print(f"{fr}[-] Error fetching WordPress users: {e}{fw}")

    # Fetch authors from REST API
    authors_url = domain + "/wp-json/wp/v2/posts/"
    try:
        response = requests.get(authors_url, verify=False)
        if response.status_code == 200:
            posts = response.json()
            authors = {post['author'] for post in posts}
            if authors:
                print(f"\n{fg}[+] WordPress Authors (from REST API):{fw}")
                for author_id in authors:
                    author_url = domain + f"/wp-json/wp/v2/users/{author_id}"
                    author_response = requests.get(author_url, verify=False)
                    if author_response.status_code == 200:
                        author = author_response.json()
                        print(f"  - {author['name']} ({author['slug']})")
                    else:
                        print(f"{fr}[-] Error fetching author details for author ID {author_id}{fw}")
            else:
                print(f"{fr}[-] No WordPress authors found.{fw}")
        else:
            print(f"{fr}[-] Error fetching WordPress posts: Status code {response.status_code}{fw}")
    except requests.exceptions.RequestException as e:
        print(f"{fr}[-] Error fetching WordPress posts: {e}{fw}")

    # Fetch authors from RSS feed
    rss_url = domain + "/feed/"
    try:
        response = requests.get(rss_url, verify=False)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            namespace = {'content': 'http://purl.org/rss/1.0/modules/content/', 'dc': 'http://purl.org/dc/elements/1.1/'}
            authors = set()
            for item in root.findall('channel/item'):
                author = item.find('dc:creator', namespace)
                if author is not None:
                    authors.add(author.text)
            if authors:
                print(f"\n{fg}[+] WordPress Authors (from RSS feed):{fw}")
                for author in authors:
                    print(f"  - {author}")
            else:
                print(f"{fr}[-] No WordPress authors found in RSS feed.{fw}")
        else:
            print(f"{fr}[-] Error fetching RSS feed: Status code {response.status_code}{fw}")
    except requests.exceptions.RequestException as e:
        print(f"{fr}[-] Error fetching RSS feed: {e}{fw}")
    except ET.ParseError as e:
        print(f"{fr}[-] Error parsing RSS feed: {e}{fw}")

      

def check_plugins_and_themes(domain, cookies):
    try:
        response = requests.get(domain, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        plugins = set(re.findall(r'wp-content/plugins/([a-zA-Z0-9_-]+)/', response.text))
        themes = set(re.findall(r'wp-content/themes/([a-zA-Z0-9_-]+)/', response.text))
        if plugins:
            print(f"{Fore.GREEN}[+] Installed Plugins:{Fore.WHITE}")
            for plugin in plugins:
                print(f"  - {plugin}")
        else:
            print(f"{Fore.RED}[-] No plugins found.{Fore.WHITE}")
        if themes:
            print(f"{Fore.GREEN}[+] Installed Themes:{Fore.WHITE}")
            for theme in themes:
                print(f"  - {theme}")
        else:
            print(f"{Fore.RED}[-] No themes found.{Fore.WHITE}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error checking plugins and themes: {e}{Fore.WHITE}")

def validate_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print(f"{Fore.GREEN}[+] SSL/TLS certificate details:{Fore.WHITE}")
                for key, value in cert.items():
                    print(f"  - {key}: {value}")
    except socket.gaierror as e:
        print(f"{Fore.RED}[-] Error validating SSL/TLS certificate: {e}{Fore.WHITE}")
    except Exception as e:
        print(f"{Fore.RED}[-] SSL/TLS validation error: {e}{Fore.WHITE}")

def check_cors(domain):
    try:
        headers = {'Origin': 'http://evil.com'}
        response = requests.get(domain, headers=headers, verify=False)
        if 'Access-Control-Allow-Origin' in response.headers and response.headers['Access-Control-Allow-Origin'] == '*':
            print(f"{fg}[-] CORS vulnerability detected!{fw}")
        else:
            print(f"{fr}[+] No CORS vulnerability detected.{fw}")
    except requests.exceptions.RequestException as e:
        print(f"{fr}Error checking CORS: {e}{fw}")

def check_security_txt(domain):
    check_path(domain, "/.well-known/security.txt", {}, {})

def check_captcha(domain, headers, cookies):
    try:
        response = requests.get(domain, headers=headers, cookies=cookies, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        found_captcha = False
        found_cloudflare = False

        for form in forms:
            if 'captcha' in str(form).lower():
                print(f"{fg}[+] Captcha found in form{fw}")
                found_captcha = True
                break
        if not found_captcha:
            print(f"{fr}[-] No Captcha found in forms{fw}")

        if 'cf-challenge' in response.text.lower() or 'cloudflare' in response.text.lower():
            print(f"{fg}[+] Cloudflare protection detected{fw}")
            found_cloudflare = True
        if not found_cloudflare:
            print(f"{fr}[-] No Cloudflare protection detected{fw}")

    except requests.exceptions.RequestException as e:
        print(f"{fr}[-] Error checking for Captcha or Cloudflare: {e}{fw}")
