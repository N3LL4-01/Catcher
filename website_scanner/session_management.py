from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style
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
    geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver.exe')
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

    vulnerable = False

    for payload in injection_payloads:
        try:
            response = requests.get(f"{domain}/?id={payload}", timeout=10)
            if any(error in response.text.lower() for error in ["sql syntax", "mysql", "syntax error"]):
                print(f"{Fore.RED}[-] Possible SQL injection vulnerability detected with payload: {payload}{Fore.WHITE}")
                vulnerable = True
        except requests.RequestException as e:
            print(f"{Fore.RED}[-] Error testing payload {payload}: {e}{Fore.WHITE}")

    if not vulnerable:
        print(f"{Fore.GREEN}[+] No SQL injection vulnerabilities detected.{Fore.WHITE}")