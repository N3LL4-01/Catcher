# path_checker.py

import re
import requests
from colorama import Fore

def check_path(domain, path, headers, cookies):
    url = f"{domain.rstrip('/')}/{path.lstrip('/')}" 
    try:
        response = requests.get(url, headers=headers, cookies=cookies, verify=False, allow_redirects=True, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Accessible path found: {url}{Fore.WHITE}")
            if path.lstrip('/') == "robots.txt":
                print(f"\n{Fore.GREEN}Contents of robots.txt:{Fore.WHITE}\n{response.text}\n")
            emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text))
            if emails:
                print(f"{Fore.GREEN}[+] Emails found in {path}:{Fore.WHITE}")
                for email in emails:
                    print(f"  - {email}")
        else:
            print(f"{Fore.RED}[-] Path not found: {path}{Fore.WHITE}")
    except requests.exceptions.TooManyRedirects:
        print(f"{Fore.RED}[-] Too many redirects at: {url}{Fore.WHITE}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] Error checking path {path}: {e}{Fore.WHITE}")
