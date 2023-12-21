from selenium.webdriver.common.by import By


class ProductPageLocator:
    main_image = (By.CSS_SELECTOR, "div.fotorama__stage__frame img")
    image_list = (By.CSS_SELECTOR, 'div.fotorama__thumb img')
    description = (By.ID, 'product.info.description')
    images_description = (By.CSS_SELECTOR, '#product\\.info\\.description img')


class TripAdvisorLocator:
    results = (By.CSS_SELECTOR, '[data-test$="_list_item"]')
    next_page = (By.CSS_SELECTOR, '.pagination .next')
    result_count = (By.CSS_SELECTOR, '#component_36 > div:nth-child(1) > div.Qqvnh > div.EaRai.Gh > span.SgeRJ > span > span')
    current_page = (By.CSS_SELECTOR, '.pagination .pageNumbers .current')
    pagination = (By.CSS_SELECTOR, '.deckTools .pagination')


class TripAdvisorDetailsLocator:
    name = (By.CSS_SELECTOR, "[data-test-target='top-info-header']")
    address = (By.CSS_SELECTOR, "[href='#MAPVIEW']")
    tel = (By.CSS_SELECTOR, "[href*='tel:']")
    email = (By.CSS_SELECTOR, "[href^='mailto:']")
    see_all_image = (By.CSS_SELECTOR, "div[onclick*='openPhotoViewer()']")
    close_image_viewer = (By.CSS_SELECTOR, "div.ui_close_x:nth-child(2)")
    photos = (By.CSS_SELECTOR, "img[onload]")
    rating = (By.XPATH, '//*[contains(text(), "Ratings and reviews")]/following-sibling::div/span[1]')
    review_count = (By.XPATH, '//*[contains(text(), "Ratings and reviews")]/following-sibling::div/a')
    price_range = (By.XPATH, '//*[contains(text(), "PRICE RANGE")]/following-sibling::div')
    cuisines = (By.XPATH, '//*[contains(text(), "CUISINES")]/following-sibling::div')
    view_all_detail = (By.XPATH, '//a[contains(text(), "View all details")]')
    about = (By.XPATH, '//div[contains(text(), "About")]/following-sibling::div')
    special_diets = (By.XPATH, '//div[contains(text(), "Special Diets")]/following-sibling::div')
    meals = (By.XPATH, '//div[contains(text(), "Meals")]/following-sibling::div')
    features = (By.XPATH, '//div[contains(text(), "FEATURES")]/following-sibling::div')
