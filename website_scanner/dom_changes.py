from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style
import requests
import os
import platform


fg = Fore.GREEN
fr = Fore.RED
fw = Fore.WHITE
fy = Fore.YELLOW
fo = Fore.LIGHTYELLOW_EX
flc = Fore.CYAN
bd = Style.BRIGHT
res = Style.RESET_ALL

def check_dom_changes(domain):
    os_type = platform.system()
    if os_type == "Windows":
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver.exe')
    elif os_type in ["Linux", "Darwin"]:  
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver')
    else:
        raise Exception(f"Unsupported OS: {os_type}")

    service = FirefoxService(executable_path=geckodriver_path)
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(service=service, options=options)
    try:
        driver.get(domain)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        scripts = soup.find_all('script')
        insecure_scripts = [script.get('src') for script in scripts if script.get('src') and 'http://' in script['src']]

        stylesheets = soup.find_all('link', rel='stylesheet')
        insecure_stylesheets = [link.get('href') for link in stylesheets if link.get('href') and 'http://' in link['href']]

        iframes = soup.find_all('iframe')
        insecure_iframes = [iframe.get('src') for iframe in iframes if iframe.get('src') and 'http://' in iframe['src']]

        if insecure_scripts or insecure_stylesheets or insecure_iframes:
            print(f"{fr}[-] Insecure elements detected in DOM:{fw}")

            if insecure_scripts:
                print(f"{fr}[-] Insecure scripts:{fw}")
                for src in insecure_scripts:
                    print(f"  - {src}")

            if insecure_stylesheets:
                print(f"{fr}[-] Insecure stylesheets:{fw}")
                for href in insecure_stylesheets:
                    print(f"  - {href}")

            if insecure_iframes:
                print(f"{fr}[-] Insecure iframes:{fw}")
                for src in insecure_iframes:
                    print(f"  - {src}")
        else:
            print(f"{fr}[+] No insecure elements found in DOM.{fw}")

    except Exception as e:
        print(f"{fg}[-] Error checking DOM changes: {e}{fw}")

    finally:
        driver.quit()

def dom(response):
    end, red, yellow = '*', '*', '*'
    highlighted = []
    sources = r'''\b(?:document\.(URL|documentURI|URLUnencoded|baseURI|cookie|referrer)|location\.(href|search|hash|pathname)|window\.name|history\.(pushState|replaceState)(local|session)Storage)\b'''
    sinks = r'''\b(?:eval|evaluate|execCommand|assign|navigate|getResponseHeaderopen|showModalDialog|Function|set(Timeout|Interval|Immediate)|execScript|crypto.generateCRMFRequest|ScriptElement\.(src|text|textContent|innerText)|.*?\.onEventName|document\.(write|writeln)|.*?\.innerHTML|Range\.createContextualFragment|(document|window)\.location)\b'''
    scripts = re.findall(r'(?i)(?s)<script[^>]*>(.*?)</script>', response)
    sinkFound, sourceFound = False, False
    for script in scripts:
        script = script.split('\n')
        num = 1
        allControlledVariables = set()
        try:
            for newLine in script:
                line = newLine
                parts = line.split('var ')
                controlledVariables = set()
                if len(parts) > 1:
                    for part in parts:
                        for controlledVariable in allControlledVariables:
                            if controlledVariable in part:
                                controlledVariables.add(re.search(r'[a-zA-Z$_][a-zA-Z0-9$_]+', part).group())
                pattern = re.finditer(sources, newLine)
                for grp in pattern:
                    if grp:
                        source = newLine[grp.start():grp.end()].replace(' ', '')
                        if source:
                            if len(parts) > 1:
                                for part in parts:
                                    if source in part:
                                        controlledVariables.add(re.search(r'[a-zA-Z$_][a-zA-Z0-9$_]+', part).group())
                            line = line.replace(source, yellow + source + end)
                for controlledVariable in controlledVariables:
                    allControlledVariables.add(controlledVariable)
                for controlledVariable in allControlledVariables:
                    matches = list(filter(None, re.findall(r'\b%s\b' % controlledVariable, line)))
                    if matches:
                        sourceFound = True
                        line = re.sub(r'\b%s\b' % controlledVariable, yellow + controlledVariable + end, line)
                pattern = re.finditer(sinks, newLine)
                for grp in pattern:
                    if grp:
                        sink = newLine[grp.start():grp.end()].replace(' ', '')
                        if sink:
                            line = line.replace(sink, red + sink + end)
                            sinkFound = True
                if line != newLine:
                    highlighted.append('%-3s %s' % (str(num), line.lstrip(' ')))
                num += 1
        except MemoryError:
            pass
    if sinkFound or sourceFound:
        return highlighted
    else:
        return []
