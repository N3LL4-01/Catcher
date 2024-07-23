from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from colorama import init, Fore, Style


fg = Fore.GREEN
fr = Fore.RED
fw = Fore.WHITE
fy = Fore.YELLOW
fo = Fore.LIGHTYELLOW_EX
flc = Fore.CYAN
bd = Style.BRIGHT
res = Style.RESET_ALL

def test_waf_bypass(domain):
    payloads = ["<script>alert('XSS')</script>", "' OR '1'='1"]
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    try:
        for payload in payloads:
            test_url = f"{domain}?test={payload}"
            driver.get(test_url)
            if payload in driver.page_source:
                print(f"{fg}[+] WAF bypassed with payload: {payload}{fw}")
            else:
                print(f"{fr}[-] Payload not detected: {payload}{fw}")
    except Exception as e:
        print(f"{fr}[-] Error testing WAF bypass: {e}{fw}")
    finally:
        driver.quit()