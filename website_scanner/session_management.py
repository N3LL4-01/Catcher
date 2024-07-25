from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style
from bs4 import BeautifulSoup
import platform
import requests
import os

fg = Fore.GREEN
fr = Fore.RED
fw = Fore.WHITE
fy = Fore.YELLOW
fo = Fore.LIGHTYELLOW_EX
flc = Fore.CYAN
bd = Style.BRIGHT
res = Style.RESET_ALL

def check_session_management(domain):
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
    try:
        login_paths = [
            "login",
            "wp-login.php",
            "admin",
            "user/login",
            "signin"
        ]

        login_pages = []
        for path in login_paths:
            full_url = f"{domain}/{path}"
            response = requests.get(full_url, verify=False)
            if response.status_code == 200:
                driver.get(full_url)
                if any(keyword in driver.title.lower() for keyword in ["login", "sign in", "anmelden", "einloggen"]):
                    login_pages.append(full_url)
                    print(f"{fg}[+] Login page found at: {full_url}{fw}")

        if not login_pages:
            print(f"{fy}[-] No login pages found.{fw}")
    except Exception as e:
        print(f"{fr}[-] Error checking session management: {e}{fw}")
    finally:
        driver.quit()

def extract_social_links(domain):
    social_links = {
        'facebook': [],
        'twitter': [],
        'instagram': [],
        'youtube': [],
        'linkedin': [],
        'pinterest': [],
        'github': []
    }

    try:
        response = requests.get(domain, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if "facebook.com" in href:
                social_links['facebook'].append(href)
            elif "twitter.com" in href:
                social_links['twitter'].append(href)
            elif "instagram.com" in href:
                social_links['instagram'].append(href)
            elif "youtube.com" in href:
                social_links['youtube'].append(href)
            elif "linkedin.com" in href:
                social_links['linkedin'].append(href)
            elif "pinterest.com" in href:
                social_links['pinterest'].append(href)
            elif "github.com" in href:
                social_links['github'].append(href)

        if any(social_links.values()):
            print(f"{fg}[+] Social media links found:{fw}")
            for platform, links in social_links.items():
                for link in links:
                    print(f"{fo}{platform.capitalize()}: {fw}{link}")
        else:
            print(f"{fy}[-] No social media links found.{fw}")

    except requests.RequestException as e:
        print(f"{fr}[-] Error extracting social links: {e}{fw}")

def check_sql_injection(domain):
    injection_payloads = ["' OR '1'='1", "' OR '1'='1' --", "'"]
    query_params = ["id", "name", "search", "q", "query"]
    sql_error_indicators = ["sql syntax", "mysql", "syntax error"]

    vulnerable = False
    headers = {'User-Agent': 'Mozilla/5.0'}

    for payload in injection_payloads:
        for param in query_params:
            try:
                test_url = f"{domain}/?{param}={payload}"
                response = requests.get(test_url, headers=headers, timeout=10)
                if any(error in response.text.lower() for error in sql_error_indicators):
                    print(f"{fr}[-] Possible SQL injection vulnerability detected with payload: {payload} on parameter: {param}{fw}")
                    vulnerable = True
            except requests.RequestException as e:
                print(f"{fr}[-] Error testing payload {payload} on parameter {param}: {e}{fw}")

    if not vulnerable:
        print(f"{fg}[+] No SQL injection vulnerabilities detected.{fw}")

