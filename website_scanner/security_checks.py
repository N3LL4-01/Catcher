import re
import os
import socket
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from website_scanner.utils import check_captcha, check_security_txt, validate_ssl, check_cors, detect_cms, get_webserver_info, get_os_info, get_php_version, get_ip, mx_lookup, check_path, check_plugins_and_themes, scrape_wordpress_users
from website_scanner.check_file_uploads_and_xss import check_file_uploads_and_xss
from website_scanner.vulnerabilities import detect_vulnerabilities
from website_scanner.session_management import check_session_management,  check_sql_injection, extract_social_links
from website_scanner.dom_changes import check_dom_changes
from website_scanner.waf_bypass import test_waf_bypass
import warnings
from website_scanner.CMS.wix import check_wix_paths
from website_scanner.CMS.wordpress import check_wordpress_paths
from website_scanner.CMS.drupal import check_drupal_paths
from website_scanner.CMS.joomla import check_joomla_paths
from website_scanner.CMS.typo3 import check_typo3_paths
from website_scanner.CMS.magento import check_magento_paths
from urllib3.exceptions import InsecureRequestWarning


def scrape_info(domain, cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, wie Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(domain, headers=headers, cookies=cookies, verify=False, allow_redirects=True, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            cms, version, cms_info = detect_cms(response, domain)
            if cms != "Unknown":
                print(f"{Fore.GREEN}[+] CMS Detected:{Fore.WHITE} {cms} (Version: {version})")
                print(f"{Fore.GREEN}[+] CMS Info:{Fore.WHITE}")
                print(f"  - Template: {cms_info.get('template', 'N/A')}")
                print(f"  - Plugins: {', '.join(set(cms_info.get('plugins', [])))}")  # Remove duplicates
                print(f"  - Security Headers: {cms_info.get('security_headers', 'N/A')}")
                print(f"  - File Upload Vulnerability: {cms_info.get('file_upload_vulnerability', 'N/A')}")
            else:
                print(f"{Fore.RED}[-] No CMS detected.{Fore.WHITE}")

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

            emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a.z]{2,}\b', response.text))
            if emails:
                print(f"{Fore.GREEN}[+] Emails found:{Fore.WHITE}")
                for email in emails:
                    print(f"  - {email}")
            else:
                print(f"{Fore.RED}[-] No emails found.{Fore.WHITE}")

            impressum_links = soup.find_all('a', href=True)
            found_impressum = False
            for link in impressum_links:
                href = link['href'].lower()
                if any(keyword in href for keyword in ['impressum', 'legal', 'kontakt', 'contact']):
                    impressum_url = link['href']
                    if not impressum_url.startswith('http'):
                        impressum_url = os.path.join(domain, impressum_url)
                    try:
                        imp_response = requests.get(impressum_url, headers=headers, cookies=cookies, verify=False, allow_redirects=True, timeout=10)
                        if imp_response.status_code == 200:
                            imp_text = imp_response.text
                            # Suche nach E-Mails
                            imp_emails = set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a.z]{2,}\b', imp_text))
                            if imp_emails:
                                print(f"{Fore.GREEN}[+] Emails found in Impressum/Legal Notice/Contact:{Fore.WHITE}")
                                for email in imp_emails:
                                    print(f"  - {email}")
                            else:
                                print(f"{Fore.RED}[-] No emails found in Impressum/Legal Notice/Contact.{Fore.WHITE}")
                        else:
                            print(f"{Fore.RED}[-] Error fetching Impressum/Legal Notice/Contact: Status code {imp_response.status_code}{Fore.WHITE}")
                    except requests.exceptions.TooManyRedirects:
                        print(f"{Fore.RED}[-] Too many redirects at: {impressum_url}{Fore.WHITE}")
                    except requests.exceptions.RequestException as e:
                        print(f"{Fore.RED}[-] Error fetching Impressum/Legal Notice/Contact: {e}{Fore.WHITE}")
                    found_impressum = True
                    break

            validate_ssl(domain)
            mx_lookup(domain.replace("http://", "").replace("https://", "").replace("/", ""))
            detect_vulnerabilities(cms, version)
            check_security_txt(domain)
            check_cors(domain)
            scrape_wordpress_users(domain)

            if not found_impressum:
                print(f"{Fore.RED}[-] No Impressum/Legal Notice found.{Fore.WHITE}")

            # CMS-spezifische Überprüfungen
            if cms == 'WordPress':
                check_wordpress_paths(domain, headers, cookies)
            elif cms == 'Joomla':
                check_joomla_paths(domain, headers, cookies)
            elif cms == 'Drupal':
                check_drupal_paths(domain, headers, cookies)
            elif cms == 'Typo3':
                check_typo3_paths(domain, headers, cookies)
            elif cms == 'Magento':
                check_magento_paths(domain, headers, cookies)
            elif cms == 'Wix':
                check_wix_paths(domain, headers, cookies)

            if cookies:
                print(f"{Fore.CYAN}---------------------------------------{Fore.WHITE}")
                print(f"{Fore.MAGENTA}        SECURITY INFORMATION         {Fore.WHITE}")
                print(f"{Fore.CYAN}---------------------------------------{Fore.WHITE}")
                check_plugins_and_themes(domain, cookies)
                extract_social_links(domain)
                check_captcha(domain, headers, cookies)
                check_dom_changes(domain)
                test_waf_bypass(domain)
                check_session_management(domain)
                check_sql_injection(domain)
            else:
                print(f"{Fore.YELLOW}Skipping checks that require cookies.{Fore.WHITE}")

            #check_file_uploads_and_xss(domain, cookies, headers)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] Error during scraping: {e}{Fore.WHITE}")
