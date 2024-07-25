# Catcher - Web Vulnerability Scanner

<p align="center">
  <pre>
  ______        __  ___________  ______    __    __    _______   _______   
 /" _  "\      /""\("     _   ")/" _  "\  /" |  | "\  /"     "| /"      \  
(: ( \___)    /    \)__/  \\__/(: ( \___)(:  (__)  :)(: ______)|:        | 
 \/ \        /' /\  \  \\_ /    \/ \      \/      \/  \/    |  |_____/   ) 
 //  \ _    //  __'  \ |.  |    //  \ _   //  __  \\  // ___)_  //      /  
(:   _) \  /   /  \\  \\:  |   (:   _) \ (:  (  )  :)(:      "||:  __   \  
 \_______)(___/    \___)\__|    \_______) \__|  |__/  \_______)|__|  \___)                                                                     
  </pre>
</p>

## DISCLAIMER - It's a community project and not finished yet!





https://github.com/user-attachments/assets/11c0aa79-9b70-49d7-a87d-6c9e25826e9d



Catcher is a web vulnerability scanner that detects security holes in web applications. It supports the detection of CMS, XSS, unsafe file uploads and many other vulnerabilities. Please remember that it is a tool that provides you with the relevant information at first glance to give you an idea of ​​your target domain. It does NOT replace a professional scan! It is intended as an aid!

## Goal-Features

- **CMS Detection**: Detects popular CMS like WordPress, Joomla, Drupal, and Typo3. 
- **File Upload Checks**: Checks for insecure file uploads and configuration files. 
- **XSS Detection**: Detects Cross-Site Scripting (XSS) vulnerabilities.
- **SQL Injection**: Checks for simple SQL injection vulnerabilities.
- **Session Management**: Checks for session management vulnerabilities. 
- **DOM Changes**: Analyzes insecure elements in the DOM. 
- **Captcha Detection**: Detects missing captchas in forms.
- **Cookie Grabbing**: Collects cookies from the domain for further analysis.
- **Domain Information**: Provides initial domain information like IP address, server details, etc.


## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/N3LL4-01/Catcher.git
    cd Catcher
    ```

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download Geckodriver:**
    Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) and place it in the `website_scanner` directory.

4. **Set executable permissions for Geckodriver (macOS/Linux users only):**
    ```bash
    chmod +x path/to/geckodriver
    ```

## Usage

1. **Start the scanner:**
    ```bash
    python run.py
    ```

2. **Follow the prompts:**
    Enter the domain to scan (including `http://` or `https://`).

