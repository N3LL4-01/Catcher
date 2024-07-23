import re
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from website_scanner.utils import check_captcha, check_security_txt, validate_ssl, check_cors, detect_cms, get_webserver_info, get_os_info, get_php_version, get_ip, check_path, check_plugins_and_themes, scrape_wordpress_users
from website_scanner.check_file_uploads_and_xss import check_file_uploads_and_xss
from website_scanner.vulnerabilities import detect_vulnerabilities
from website_scanner.session_management import check_session_management,  check_sql_injection
from website_scanner.dom_changes import check_dom_changes
import warnings
from urllib3.exceptions import InsecureRequestWarning

def scrape_info(domain, cookies):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    try:
        response = requests.get(domain, headers=headers, cookies=cookies, verify=False, allow_redirects=True, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            cms, version = detect_cms(response)
            print(f"{Fore.GREEN}[+] CMS Detected:{Fore.WHITE} {cms} (Version: {version})")

            server, x_powered_by = get_webserver_info(response.headers)
            print(f"{Fore.GREEN}[+] Web Server:{Fore.WHITE} {server}")
            print(f"{Fore.GREEN}[+] X-Powered-By:{Fore.WHITE} {x_powered_by}")

            os_info = get_os_info(response)
            print(f"{Fore.GREEN}[+] Server OS:{Fore.WHITE} {os_info}")

            php_version = get_php_version(response.headers)
            print(f"{Fore.GREEN}[+] PHP Version:{Fore.WHITE} {php_version}")

            ip = get_ip(domain.replace("http://", "").replace("https://", "").replace("/", ""))
            print(f"{Fore.GREEN}[+] IP Address:{Fore.WHITE} {ip}")

            check_path(domain, "/robots.txt", headers, cookies)

            emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text))
            if emails:
                print(f"{Fore.GREEN}[+] Emails found:{Fore.WHITE}")
                for email in emails:
                    print(f"  - {email}")
            else:
                print(f"{Fore.RED}[-] No emails found.{Fore.WHITE}")

            impressum_links = soup.find_all('a', href=True)
            found_impressum = False
            for link in impressum_links:
                if 'impressum' in link['href'].lower():
                    impressum_url = link['href']
                    if not impressum_url.startswith('http'):
                        impressum_url = os.path.join(domain, impressum_url)
                    try:
                        imp_response = requests.get(impressum_url, headers=headers, cookies=cookies, verify=False, allow_redirects=True, timeout=10)
                        if imp_response.status_code == 200:
                            imp_emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', imp_response.text))
                            if imp_emails:
                                print(f"{Fore.GREEN}[+] Emails found in Impressum:{Fore.WHITE}")
                                for email in imp_emails:
                                    print(f"  - {email}")
                            else:
                                print(f"{Fore.RED}[-] No emails found in Impressum.{Fore.WHITE}")
                        else:
                            print(f"{Fore.RED}[-] Error fetching Impressum: Status code {imp_response.status_code}{Fore.WHITE}")
                    except requests.exceptions.TooManyRedirects:
                        print(f"{Fore.RED}[-] Too many redirects at: {impressum_url}{Fore.WHITE}")
                    except requests.exceptions.RequestException as e:
                        print(f"{Fore.RED}[-] Error fetching Impressum: {e}{Fore.WHITE}")
                    found_impressum = True
                    break


            validate_ssl(domain)
            detect_vulnerabilities(cms, version)
            check_security_txt(domain)
            check_cors(domain)
            scrape_wordpress_users(domain) 

            if not found_impressum:
                print(f"{Fore.RED}[-] No Impressum found.{Fore.WHITE}")
    

            if cms == 'WordPress':
                wp_paths = [
                    'wp-includes/', 'wp-includes/images/', 'wp-content/',
                    'wp-content/uploads/', 'wp-content/themes/', 'wp-content/plugins/',
                    'wp-content/plugins/hustle/views/admin/dashboard/', 'wp-admin/',
                    'wp-cron.php', 'readme.html', 'xmlrpc.php'
                ]
                for path in wp_paths:
                    check_path(domain, path, headers, cookies)

                #scrape_wordpress_users(domain)

            elif cms == 'Joomla':
                joomla_paths = [
                    'administrator/', 'components/', 'images/', 'includes/',
                    'language/', 'libraries/', 'media/', 'modules/',
                    'plugins/', 'templates/'
                ]
                for path in joomla_paths:
                    check_path(domain, path, headers, cookies)

            elif cms == 'Drupal':
                drupal_paths = [
                    'core/', 'modules/', 'profiles/', 'sites/',
                    'themes/'
                ]
                for path in drupal_paths:
                    check_path(domain, path, headers, cookies)

            elif cms == 'Typo3':
                typo3_paths = [
                    'typo3/', 'typo3conf/', 'typo3temp/', 'typo3_src/', 'uploads/'
                ]
                for path in typo3_paths:
                    check_path(domain, path, headers, cookies)

            elif cms == 'Magento':
                magento_paths = [
                    'pub/static/', 'var/log/', 'app/etc/', 'vendor/',
                    'pub/media/', 'app/code/', 'setup/'
                ]
                for path in magento_paths:
                    check_path(domain, path, headers, cookies)

            elif cms == 'Wix':
                print(f"{Fore.GREEN}[+] Wix CMS detected; limited checks due to the nature of Wix{Fore.WHITE}")

            print(f"\n{Fore.CYAN}-----------------------------------{Fore.WHITE}")

            if cookies:
                check_plugins_and_themes(domain, cookies)
                #check_file_uploads_and_xss(domain, cookies, headers)
                check_captcha(domain, headers, cookies)
                check_dom_changes(domain)
                check_session_management(domain)
            else:
                print(f"{Fore.YELLOW}Skipping checks that require cookies.{Fore.WHITE}")
                
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] Error during scraping: {e}{Fore.WHITE}")
