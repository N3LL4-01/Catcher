import socket
import ssl
import re
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup

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
        "                                              ",
        "                                              ",
        "                           ─▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───",
        "                         ───█▒▒░░░░░░░░░▒▒█───",
        "                         ────█░░█░░░░░█░░█────",
        "                         ─▄▄──█░░░▀█▀░░░█──▄▄─",
        "                         █░░█─▀▄░░░░░░░▄▀─█░░█",
        "                         █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█",
        "                         █░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█",
        "                         █░░║║║╠─║─║─║║║║║╠─░░█",
        "                         █░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█",
        "                         █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█",
        "        @@@@@@@  @@@@@@  @@@@@@@  @@@@@@@ @@@  @@@ @@@@@@@@ @@@@@@@ ",
        "        !@@      @@!  @@@   @@!   !@@      @@!  @@@ @@!      @@!  @@@",
        "        !@!      @!@!@!@!   @!!   !@!      @!@!@!@! @!!!:!   @!@!!@! ",
        "        :!!      !!:  !!!   !!:   :!!      !!:  !!! !!:      !!: :!! ",
        "        :: :: :  :   : :    :     :: :: :  :   : : : :: :::  :   : :",
        "                                                                ",
        "                          @n3ll41 v.0.1                          ",
        "                                                 "
    ]

    for line in logo:
        colored_line = ""
        for char in line:
            if char == '█' or char == '@':
                colored_line += logo_magenta + char
            elif  char == ':' or char == '.':
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
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    cookies = {}
    try:
        driver.get(domain)
        for cookie in driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
    except Exception as e:
        print(f"{fr}[-] Error collecting cookies: {e}{fw}")
    finally:
        driver.quit()
    
    return cookies


def detect_cms(response):
    cms = "Unknown"
    version = "Not detected"
    headers = response.headers
    html = response.text
    
    if 'x-powered-by' in headers:
        powered_by = headers['x-powered-by'].lower()
        if 'wordpress' in powered_by:
            cms = 'WordPress'
        elif 'joomla' in powered_by:
            cms = 'Joomla'
        elif 'drupal' in powered_by:
            cms = 'Drupal'
        elif 'typo3' in powered_by:
            cms = 'Typo3'
        elif 'wix' in powered_by:
            cms = 'Wix'
        elif 'magento' in powered_by:
            cms = 'Magento'
    if 'generator' in headers:
        generator = headers['generator'].lower()
        if 'wordpress' in generator:
            cms = 'WordPress'
            version = generator.split(' ')[-1]
        elif 'joomla' in generator:
            cms = 'Joomla'
            version = generator.split(' ')[-1]
        elif 'drupal' in generator:
            cms = 'Drupal'
            version = generator.split(' ')[-1]
        elif 'typo3' in generator:
            cms = 'Typo3'
            version = generator.split(' ')[-1]
        elif 'wix' in generator:
            cms = 'Wix'
        elif 'magento' in generator:
            cms = 'Magento'
            version = generator.split(' ')[-1]
    elif 'wordpress' in html.lower():
        cms = 'WordPress'
        version_search = re.search(r'content="WordPress (\d+\.\d+(\.\d+)?)"', html)
        if version_search:
            version = version_search.group(1)
    elif 'joomla' in html.lower():
        cms = 'Joomla'
        version_search = re.search(r'content="Joomla! - Open Source Content Management - (\d+\.\d+(\.\d+)?)"', html)
        if version_search:
            version = version_search.group(1)
    elif 'drupal' in html.lower():
        cms = 'Drupal'
    elif 'typo3' in html.lower():
        cms = 'Typo3'
    elif 'wix' in html.lower():
        cms = 'Wix'
    elif 'magento' in html.lower():
        cms = 'Magento'
        version_search = re.search(r'Magento (\d+\.\d+(\.\d+)?)', html)
        if version_search:
            version = version_search.group(1)
    
    return cms, version

def get_php_version(headers):
    php_version = "Unknown"
    if 'x-powered-by' in headers:
        php_header = headers['x-powered-by'].lower()
        match = re.search(r'php\/(\d+\.\d+(\.\d+)?)', php_header)
        if match:
            php_version = match.group(1)
    return php_version

def get_webserver_info(headers):
    server = headers.get('Server', 'Unknown')
    x_powered_by = headers.get('X-Powered-By', 'Unknown')
    return server, x_powered_by

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

def check_path(domain, path, headers, cookies):
    url = f"{domain.rstrip('/')}/{path.lstrip('/')}" 
    try:
        response = requests.get(url, headers=headers, cookies=cookies, verify=False, allow_redirects=True, timeout=10)
        if response.status_code == 200:
            print(f"{fg}[+] Found:{fw} {path}")
            if path == "/robots.txt":
                print(f"\n{fg}Contents of robots.txt:{fw}\n{response.text}\n")
            emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text))
            if emails:
                print(f"{fg}[+] Emails found in {path}:{fw}")
                for email in emails:
                    print(f"  - {email}")
        else:
            print(f"{fr}[-] Path not found: {path}{fw}")
    except requests.exceptions.TooManyRedirects:
        print(f"{fr}[-] Too many redirects at: {url}{fw}")
    except requests.exceptions.RequestException as e:
        print(f"{fr}[-] Error checking path {path}: {e}{fw}")

def scrape_wordpress_users(domain):
    users_url = domain + "/wp-json/wp/v2/users/"
    try:
        response = requests.get(users_url, verify=False)
        if response.status_code == 200:
            users = response.json()
            if users:
                print(f"\n{fg}[+] WordPress Users:{fw}")
                for user in users:
                    print(f"  - {user['name']} ({user['slug']})")
            else:
                print(f"{fr}[-] No WordPress users found.{fw}")
        else:
            print(f"{fr}[-] Error fetching WordPress users: Status code {response.status_code}{fw}")
    except requests.exceptions.RequestException as e:
        print(f"{fr}[-] Error fetching WordPress users: {e}{fw}")        

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
        with socket.create_connection((domain, 443)) as sock:
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

def check_captcha_and_cloudflare(domain, headers, cookies):
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
