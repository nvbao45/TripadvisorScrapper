from dotenv import dotenv_values
from selenium import webdriver

config = dotenv_values("config.txt")


class FirefoxDriver:
    def __init__(self, proxy=False):
        from selenium.webdriver.firefox.options import Options
        options = Options()
        # options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def get_driver(self):
        return self.driver

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()


class ChromeDriver:
    def __init__(self, headless=True, use_proxy=False):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--window-size=1920,1080")
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-in-process-stack-traces")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # if use_proxy:
        #     options.add_argument(f"--proxy-server={config['PROXY_SERVER']}")
        self.driver = webdriver.Chrome(executable_path=config['CHROME_EXE'], options=options)

    def get_driver(self):
        return self.driver

    def check_proxy(self):
        self.driver.get("http://www.whatismyproxy.com/")

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()
