import time

from pages.base_page import BasePage
from resources.locators import TripAdvisorLocator as TAL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import utils


class TripAdvisor(BasePage):
    def __init__(self, driver, url) -> None:
        super().__init__(driver)
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url

    def get_result_count(self):
        spans = self.wait(TAL.result_count)
        if spans is not None:
            return int(spans.text)
        else:
            return -1

    def get_result_link(self):
        links = []
        count = 0
        current_page = 0
        
        total = self.get_result_count()
        with open("tmp/result_links.txt", "w") as file:
            pass
        while True:
            try:
                pagination = self.find(TAL.pagination)
                if pagination is not None:
                    while True:
                        try:
                            current = self.find(TAL.current_page)
                            if int(current.text) > current_page:
                                current_page = int(current.text)
                                break
                        except:
                            pass
                results = self.wait_all(TAL.results)
                for result in results:
                    link = result.find_element(By.CSS_SELECTOR, "a")
                    if link is not None:
                        href = link.get_attribute("href")
                        if href is not None:
                            # count += 1
                            # utils.print_progress_bar(count, total, f"{href}\nGetting link", f"{count}/{total}", length=50)
                            print(href)
                            links.append(href)
                            with open("tmp/result_links.txt", "a") as file:
                                file.write(href + "\n")

                next_button = self.find(TAL.next_page)
                if next_button is not None:
                    classes = next_button.get_attribute("class")
                    if "disabled" not in classes:
                        self.wait_click(next_button)
                    else:
                        break
                else:
                    break
            except Exception as e:
                print(e)
                break
        print("Done")
        return links
