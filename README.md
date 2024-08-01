  # Catcher - Web Vulnerability Scanner </p>

<p align="center" href="https://www.animatedimages.org/cat-lines-562.htm"><img src="https://www.animatedimages.org/data/media/562/animated-line-image-0379.gif" border="0" alt="animated-line-image-0379" /></p>

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





https://github.com/user-attachments/assets/a99549d4-b9eb-4cb3-8076-c78a45dfad3b







<p align="center">
Catcher is a web vulnerability scanner that detects security holes in web applications. It supports the detection of CMS, XSS, unsafe file uploads and many other vulnerabilities. Please remember that it is a tool that provides you with the relevant information at first glance to give you an idea of ​​your target domain. It does NOT replace a professional scan! It is intended as an aid!
</p>

<p align="center" href="https://www.animatedimages.org/cat-lines-562.htm"><img src="https://www.animatedimages.org/data/media/562/animated-line-image-0379.gif" border="0" alt="animated-line-image-0379" /></p>

## Goal-Features
- **Detects Vulnerable Cookies**: Identifies cookies that are vulnerable based on three attributes: HttpOnly, Secure, and SameSite.
- **HttpOnly**: False means the cookie is accessible via JavaScript, making it vulnerable.
- **Secure**: False indicates the cookie is not encrypted over HTTPS, making it vulnerable.
- **SameSite**: None allows the cookie to be sent with cross-site requests, making it vulnerable.
- **Cookies Collected**: Lists specific cookies and their values, which might be used for further analysis or debugging.  
![image](https://github.com/user-attachments/assets/9300434b-bba2-45ad-86b8-ac5a2b7e090e)

<p align="center" href="https://www.animatedimages.org/cat-lines-562.htm"><img src="https://www.animatedimages.org/data/media/562/animated-line-image-0379.gif" border="0" alt="animated-line-image-0379" /></p>

- **CMS Detection**: Detects popular CMS like WordPress, Joomla, Drupal, and Typo3.
- **Domain Information**: Provides initial domain information like IP address, server details,Plugins etc.
- **File Upload Checks**: Checks for insecure file uploads and configuration files.
- **XSS Detection**: Detects Cross-Site Scripting (XSS) vulnerabilities.
- **SQL Injection**: Checks for simple SQL injection vulnerabilities.
- **Session Management**: Checks for session management vulnerabilities. 
- **DOM Changes**: Analyzes insecure elements in the DOM. 
- **Captcha Detection**: Detects missing captchas in forms.

![image](https://github.com/user-attachments/assets/05f19f99-2727-40e1-bc0f-af9e4c021758)



<p align="center" href="https://www.animatedimages.org/cat-lines-562.htm"><img src="https://www.animatedimages.org/data/media/562/animated-line-image-0379.gif" border="0" alt="animated-line-image-0379" /></p>

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

