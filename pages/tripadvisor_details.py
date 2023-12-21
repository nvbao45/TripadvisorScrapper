import time
import datetime

from dotenv import dotenv_values
from pages.base_page import BasePage
from resources.locators import TripAdvisorDetailsLocator as TADL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import utils

config = dotenv_values("config.txt")


class TripAdvisorDetails(BasePage):
    def __init__(self, driver, url) -> None:
        super().__init__(driver)
        self.url = url
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url

    def title(self):
        return self.driver.title

    def get_details(self):
        while True:
            name = self.find(TADL.name)
            if name is not None:
                if name.get_attribute("innerText") is not None:
                    break
        address = self.find(TADL.address)
        tel = self.find(TADL.tel)
        email = self.find(TADL.email)
        website_url = self.find((By.CSS_SELECTOR, ".ui_icon.laptop"))
        if website_url is not None:
            website_url = website_url.find_element(By.XPATH, "..")

        see_all_image = self.find(TADL.see_all_image)
        rating = self.find(TADL.rating)
        review_count = self.find(TADL.review_count)
        price_range = self.find(TADL.price_range)
        cuisine = self.find(TADL.cuisines)
        about = None
        meals = None
        special_diets = None
        features = None

        try:
            images = []
            if config['GET_IMAGE'] == "True":
                if see_all_image is not None:
                    self.wait_click(see_all_image)
                    photos = self.wait_all(TADL.photos)
                    for photo in photos:
                        photo_src = photo.get_attribute("src")
                        if photo_src is not None:
                            photo_src = photo_src.replace("media/photo-s", "media/photo-w")
                            images.append(photo_src)
                    time.sleep(5)
                    self.find(TADL.close_image_viewer).click()
        except:
            pass
        try:
            view_all_detail = self.find(TADL.view_all_detail)
            if view_all_detail is not None:
                view_all_detail.click()
                time.sleep(0.5)
                about = self.wait(TADL.about, duration=5)
                meals = self.find(TADL.meals)
                special_diets = self.find(TADL.special_diets)
                features = self.find(TADL.features)
        except:
            pass

        _email = ''
        try:
            if email is not None:
                tmp = email.get_attribute("href")
                if tmp is not None:
                    tmp = tmp.replace("mailto:", "").replace("?subject=?", "")
                    _email = tmp
        except:
            pass

        try:
            if config['GET_EMAIL_IN_WEBSITE'] == "True":
                if _email == "" and _website_url != "":
                    try:
                        self.driver.get(_website_url)
                        time.sleep(2)
                        html = self.driver.execute_script("return document.getElementsByTagName('body')[0].innerHTML")
                        _email = utils.find_email(html)
                    except:
                        pass
        except:
            pass
            
        result = dict(
            link=self.url.strip(),
            name=str(name.get_attribute("innerText")), 
            address=address.get_attribute("innerText") if address is not None else "",
            tel=tel.get_attribute("innerText") if tel is not None else "",
            email=_email,
            rating=rating.get_attribute("innerText").strip() if rating is not None else "",
            review_count=review_count.get_attribute("innerText").strip().split(" ")[0] if review_count is not None else "",
            cuisine=cuisine.get_attribute("innerText") if cuisine is not None else "",
            price_range=price_range.get_attribute("innerText") if price_range is not None else "",
            about=about.get_attribute('innerText') if about is not None else "",
            website_url=website_url.get_attribute('href') if website_url is not None else "",
            special_diets=special_diets.get_attribute('innerText') if special_diets is not None else "",
            meals=meals.get_attribute('innerText') if meals is not None else "",
            features=features.get_attribute('innerText') if features is not None else "",
            images=images if len(images) > 0 else [],
            timestamp=datetime.datetime.now().strftime('%H:%M:%S-%Y/%m/%d')
        )

        return result
