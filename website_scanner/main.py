from website_scanner.utils import print_logo, get_cookies, get_ip
from website_scanner.security_checks import scrape_info
from website_scanner.session_management import check_session_management, check_sql_injection
from website_scanner.check_file_uploads_and_xss import check_file_uploads_and_xss
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from colorama import Fore

def run_scanner():
    print_logo()
    
    domain = input(f"{Fore.YELLOW}Please enter the domain to scan (without http/https): {Fore.WHITE}")
    if not domain.startswith('http://') and not domain.startswith('https://'):
        domain = 'http://' + domain
    
    print(f"\n{Fore.LIGHTYELLOW_EX}Starting to scan the domain:{Fore.RESET} {Fore.WHITE}{domain}{Fore.WHITE}\n")
    
    print(f"{Fore.CYAN}---------------------------------------{Fore.WHITE}")
    print(f"{Fore.MAGENTA}             COOKIE                    {Fore.WHITE}")
    print(f"{Fore.CYAN}---------------------------------------{Fore.WHITE}")
    
    cookies = get_cookies(domain)


    
    if cookies:
        print(f"{Fore.GREEN}[+] Cookies collected:{Fore.WHITE}")
        for name, value in cookies.items():
            print(f"  - {name}: {value}")
        
        print(f"{Fore.CYAN}---------------------------------------{Fore.WHITE}")
        print(f"{Fore.MAGENTA}         DOMAIN INFORMATION         {Fore.WHITE}")
        print(f"{Fore.CYAN}---------------------------------------{Fore.WHITE}")
    else:
        print(f"{Fore.RED}[-] No cookies collected. Skipping cookie-dependent checks.{Fore.WHITE}")
    
    try:
        scrape_info(domain, cookies)
    except Exception as e:
        print(f"{Fore.RED}[-] Error during scraping: {e}{Fore.WHITE}")
    
    try:
        check_session_management(domain)
    except Exception as e:
        print(f"{Fore.RED}[-] Error during session management check: {e}{Fore.WHITE}")

    try:
        check_sql_injection(domain)
    except Exception as e:
        print(f"{Fore.RED}[-] Error during SQL injection check: {e}{Fore.WHITE}")

    try:
        check_file_uploads_and_xss(domain, cookies, headers={'User-Agent': 'Mozilla/5.0'})
    except Exception as e:
        print(f"{Fore.RED}[-] Error during file uploads and XSS check: {e}{Fore.WHITE}")

if __name__ == "__main__":
    run_scanner()
