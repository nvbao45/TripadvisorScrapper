import csv
import numpy as np
import sys
import os

from utils import utils
from dotenv import dotenv_values
from resources.drivers import ChromeDriver
from pages.tripadvisor import TripAdvisor
from pages.tripadvisor_details import TripAdvisorDetails
from concurrent.futures import ThreadPoolExecutor


headers = [
    'link', 'name', 'address', 'tel', 'email',
    'rating', 'review_count', 'cuisine', 'price_range',
    'about', 'website_url', 'special_diets', 'meals',
    'features', 'images', 'timestamp'
]


def remove_duplicate_in_file(file_location):
    _tmp = []
    with open(file_location, "r") as file:
        _tmp = file.readlines()
        _tmp = list(dict.fromkeys(_tmp))
    with open(file_location, "w") as file:
        file.writelines(_tmp)


def array_split(data, n):
    return np.array_split(data, n)


def remove_all_file_in_folder(folder):
    # split_folder = os.path.join(tmp_folder, "split")
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))


def read_file(file_location):
    _result = []
    with open(file_location) as file:
        result = file.readlines()
    return result


def data_exist_in_file(data, file_location):
    with open(file_location) as file:
        file_data = file.readlines()
    if data in file_data:
        return True
    else:
        return False


def write_file(data, location):
    with open(location, "w") as file:
        file.writelines(data)


def crawler(file, _driver):
    _driver = _driver.get_driver()
    lst = read_file(file)
    global count
    global total_link
    for line in lst:
        try:
            tripadvisor = TripAdvisorDetails(_driver, line)
            details = tripadvisor.get_details()
            with open(config['OUTPUT_FILE'], 'a', newline='', encoding='utf8') as csvfile:
                count += 1
                print(f"[{count}/{total_link}] {_driver.title}")
                _writer = csv.DictWriter(csvfile, fieldnames=headers)
                _writer.writerow(details)
                with open(file.replace(".txt", "-processed.txt"), 'a') as f:
                    f.writelines(line)
        except Exception as exception:
            print(exception)
            pass
    _driver.quit()


if __name__ == "__main__":
    config = dotenv_values("config.txt")
    headless_mode = False
    use_proxy = False
    links = []
    count = 0
    total_link = 0
    resume = False
    max_thread = int(config['MAX_THREAD'])

    current_dir = os.getcwd()
    tmp_folder = os.path.join(current_dir, "tmp")
    result_link_file = os.path.join(tmp_folder, "result_links.txt")
    split_folder = os.path.join(tmp_folder, "split")

    if config['HEADLESS_MODE'] == 'True':
        headless_mode = True
    if config['USE_PROXY'] == 'True':
        use_proxy = True
        utils.enable_proxy(config['PROXY_SERVER'])

    if len(os.listdir(split_folder)) > 0:
        rs = input("Do you want to resume last progress? (Y/N): ")
        if rs.lower() == "y":
            resume = True
            processed_file = [file for file in os.listdir(split_folder) if "processed" in file]
            link_file = [file for file in os.listdir(split_folder) if "processed" not in file]
            for file in processed_file:
                id = file.split("-")[0]
                processed_link = read_file(os.path.join(split_folder, file))
                links = read_file(os.path.join(split_folder, f"{id}.txt"))
                links_not_processed = []
                for link in links:
                    if link not in processed_link:
                        links_not_processed.append(link)
                count += len(processed_link)
                write_file(links_not_processed, os.path.join(split_folder, f"{id}.txt"))
        else:
            remove_all_file_in_folder(split_folder)

    if not resume:
        url = input("Enter TripAdvisor Url: ")
        driver = ChromeDriver(headless=headless_mode)
        trip_advisor = TripAdvisor(driver.get_driver(), url)
        links = trip_advisor.get_result_link()
        driver.quit()
        remove_duplicate_in_file(result_link_file)
    data_link = read_file(result_link_file)
    total_link = len(data_link)
    if not resume:
        data_split = array_split(data_link, max_thread)
        for i in range(len(data_split)):
            write_file(data_split[i], os.path.join(split_folder, f"{i}.txt"))

    drivers = [ChromeDriver(headless=headless_mode) for _ in range(max_thread)]
    try:
        if not resume:
            with open(config['OUTPUT_FILE'], 'w', newline='', encoding='utf8') as csvfile:
                _writer = csv.DictWriter(csvfile, fieldnames=headers)
                _writer.writeheader()

        split_file = [os.path.join(split_folder, f'{i}.txt') for i in range(max_thread)]
        with ThreadPoolExecutor(max_workers=max_thread) as executor:
            bucket = executor.map(crawler, split_file, drivers)
        
        if count >= total_link:
            remove_all_file_in_folder(split_folder)
    except Exception as e:
        print(e)
        executor.shutdown()
    if use_proxy:
        utils.disable_proxy()
