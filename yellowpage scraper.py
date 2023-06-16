from math import ceil
from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup

import pandas as pd

# Required Variables
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"


def extract_info(info):
    """Extract all data in one full page"""
    business_name = info.select_one(".business-name").text
    # add category in list due to have multiple values
    category = [categories.text for categories in info.select_one(".categories")]
    # using rating_tag as a variable to avoid error
    if rating_tag := info.select_one(".result-rating"):
        word2num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        rating = word2num.get(rating_tag["class"][1])
        review = rating_tag.text
    else:
        rating, review = None, None
    # add else None in all variable to avoid Nonetype error
    phone = info.select_one(".phones")
    phone = phone.text if phone else None
    year = info.select_one(".number")
    year = year.text if year else None
    website = info.select_one(".links")
    website = website.find("a")["href"] if website and website.find("a") else None
    street = info.select_one(".street-address")
    street = street.text if street else None
    city = info.select_one(".locality")
    city = city.text if city else None
    return {
        "business_name": business_name,
        "category": category,
        "rating": rating,
        "review": review,
        "year": year,
        "website": website,
        "phone": phone,
        "street": street,
        "city": city,
    }


def main(URL: str, FILE_PATH: str):
    """This function used to start scraping process with parameter
    Url i.e yellowpages.com/ and file path i.e D:/Python Pro/Output/output.csv"""
    response = requests.get(URL, headers={"User-Agent": USER_AGENT})
    soup = BeautifulSoup(response.content, "html.parser")
    info_list = []
    page = 1
    index_tag = soup.select_one(".showing-count")
    total_index = index_tag.text.split()
    total_page = ceil(int(total_index[-1]) / 30)
    # loop all data until page reach total page
    while page <= total_page:
        sleep(randint(10, 20))
        print(f"Opening page {page}...")
        infos = soup.find_all("div", class_="result")
        info_list.extend(extract_info(info) for info in infos)
        page += 1
        # change url to next page
        url = f"{URL}?page={page}"
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        # change use new soup for new url
        soup = BeautifulSoup(response.content, "html.parser")
        print("Data Extraction Complete")
        # save data every 5 page and  last page
        if page % 5 == 0 or page == total_page:
            print("Data saving as csv")
            df = pd.DataFrame(info_list)
            df.to_csv(FILE_PATH, index=False)
            info_list = []


if __name__ == "__main__":
    URL = input("Enter yellow_page URL: ")
    FILE_PATH = input("Enter file path with filename.csv: ")
    main(URL, FILE_PATH)
