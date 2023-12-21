from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class BasePage:
    def __init__(self, driver) -> None:
        self.driver = driver

    def click(self, by_locator):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        ).click()

    def wait_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, by_locator, text):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        ).send_keys(text)

    def get_text(self, by_locator):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        ).text

    def wait(self, by_locator, duration=10):
        try:
            element = WebDriverWait(self.driver, duration).until(
                EC.visibility_of_element_located(by_locator)
            )
            return element
        except TimeoutException:
            return None

    def wait_all(self, by_locator, duration=20):
        try:
            elements = WebDriverWait(self.driver, duration).until(
                EC.visibility_of_all_elements_located(by_locator)
            )
            return elements
        except TimeoutException:
            return None

    def wait_ec(self, ec, duration=20):
        try:
            elements = WebDriverWait(self.driver, duration).until(
                ec
            )
            return elements
        except TimeoutException:
            return None

    def finds(self, by_locator):
        try:
            element = self.driver.find_elements(by_locator[0], by_locator[1])
            return element
        except NoSuchElementException:
            return None

    def find(self, by_locator):
        try:
            element = self.driver.find_element(by_locator[0], by_locator[1])
            return element
        except NoSuchElementException:
            return None


