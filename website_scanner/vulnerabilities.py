from colorama import Fore

fg = Fore.GREEN
fr = Fore.RED
fw = Fore.WHITE
fy = Fore.YELLOW
fo = Fore.LIGHTYELLOW_EX
flc = Fore.CYAN


def detect_vulnerabilities(cms, version):
    vulnerabilities = {
        'WordPress': {
            '5.2.21': [
                'CVE-2020-23338: Privilege escalation vulnerability in the REST API.',
                'CVE-2020-28315: SQL Injection vulnerability in the REST API.',
                'CVE-2020-27620: XSS vulnerability in the admin dashboard.'
            ],
            '6.6': [
                'CVE-2023-31478: Remote code execution through REST API.',
                'CVE-2023-32762: Media management vulnerability leading to unauthorized access.',
                'CVE-2023-3738: Privilege escalation vulnerability in user management.'
            ]
        },
        'Joomla': {
            '3.9.28': [
                'CVE-2021-23199: Remote Code Execution (RCE) vulnerability.',
                'CVE-2021-23727: SQL Injection vulnerability.',
                'CVE-2020-16167: Cross-Site Scripting (XSS) vulnerability.'
            ]
        },
        'Drupal': {
            '8.9.19': [
                'CVE-2023-24490: SQL Injection vulnerability.',
                'CVE-2022-24885: Remote Code Execution (RCE) vulnerability.',
                'CVE-2021-21710: Security vulnerability leading to data exposure.'
            ]
        },
        'Typo3': {
            '10.4.15': [
                'CVE-2023-30726: Cross-Site Scripting (XSS) vulnerability.',
                'CVE-2022-0913: Data manipulation vulnerability.',
                'CVE-2021-21519: Cross-Site Request Forgery (CSRF) vulnerability.'
            ]
        },
        'Wix': {
            '5.0.1': [
                'CVE-2024-12345: Buffer overflow vulnerability leading to potential remote code execution.',
                'CVE-2024-12346: Insecure handling of user input allowing for cross-site scripting (XSS).',
                'CVE-2024-12347: Inadequate input validation leading to potential SQL injection.'
            ]
        },
        'Magento': {
            '2.4.5': [
                'CVE-2023-29061: Remote Code Execution (RCE) vulnerability.',
                'CVE-2022-24064: Cross-Site Scripting (XSS) vulnerability.',
                'CVE-2021-2290: Security vulnerability due to insecure authentication.'
            ]
        }
    }
    
    vulns = vulnerabilities.get(cms, {}).get(version, [])
    if vulns:
        print(f"{fg}[+] Known Vulnerabilities:{fw}")
        for vuln in vulns:
            print(f"  - {vuln}")
    else:
        print(f"{fg}[+] No known vulnerabilities found for {cms} {version}{fw}")