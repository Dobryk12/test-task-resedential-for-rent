import json
import bs4
import asyncio
import requests
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://realtylink.org/en/properties~for-rent"
headers = {
    'User-Agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
DRIVER_PATH = r"C:\Users\Sergiy\Desktop\Progs\chromedriver-win64\chromedriver.exe"


async def get_links():
    driver = webdriver.Chrome()

    driver.get(BASE_URL)
    await asyncio.sleep(3)

    url_set = set()

    for _ in range(5):
        count = 0
        while count < 20:
            soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            addresses = soup.select(".property-thumbnail-item.thumbnailItem.col-12.col-sm-6.col-md-4.col-lg-3")

            for address in addresses:
                url_set.add("https://realtylink.org" + address.select_one(".a-more-detail").get("href"))

            count += len(addresses)

            if count < 20:
                try:
                    button = driver.find_element(By.XPATH, '//*[@id="divWrapperPager"]/ul/li[4]/a')
                    button.click()
                    await asyncio.sleep(3)
                except:
                    print("No button")

    driver.quit()

    url_links = list(url_set)
    print(len(url_links))
    return url_links[:60]


def get_title(soup):
    return soup.select_one(".col.text-left.pl-0 > h1 > span").text


def get_region(soup):
    region_parts = [part.strip() for part in soup.select_one(".pt-1").text.strip().split(",")[-2:]]
    return ', '.join(region_parts)


def get_address(soup):
    return ', '.join(soup.select_one(".pt-1").text.strip().split(",")[:-2])


def get_description(soup):
    description_row = soup.find(itemprop="description")
    if description_row:
        return description_row.text.strip()
    else:
        return "No description"


async def get_images(soup, link):
    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(link)
        wait = WebDriverWait(driver, 10)
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="overview"]/div[2]/div[1]/div/div[3]/button')))
        if button:
            button.click()
            await asyncio.sleep(1)

            soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            li_tags = soup.find_all('li', style=True)
            image_urls = [img['src'] for li in li_tags for img in li.find_all('img', src=True)]
            image_urls = [url if url.strip() else "Посилання на зображення відсутнє" for url in image_urls]

        else:
            image_urls = ["Фотографії відсутні"]
    except TimeoutException:
        image_urls = ["Фотографії відсутні"]

    finally:
        driver.quit()

    return image_urls


def get_price(soup):
    spans = soup.find_all('span', class_='text-nowrap')
    return "".join(spans[1].get_text().split())


def get_rooms(soup):
    bedrooms = soup.select_one(".col-lg-3.col-sm-6.cac")
    bathrooms = soup.select_one(".col-lg-3.col-sm-6.sdb")

    if bedrooms and bathrooms:
        return int(bedrooms.text.strip()[0]) + int(bathrooms.text.strip()[0])
    elif bedrooms:
        return int(bedrooms.text.strip()[0])
    elif bathrooms:
        return int(bathrooms.text.strip()[0])
    else:
        return "No rooms"


def get_square(soup):
    return soup.select_one(".carac-value > span").text.strip()


async def parse_all_data():
    data = []
    links = await get_links()
    for link in links:
        page = requests.get(link, headers=headers).content
        soup = bs4.BeautifulSoup(page, 'html.parser')

        property_data = {
            "link": link,
            'title': get_title(soup),
            'region': get_region(soup),
            'address': get_address(soup),
            'description': get_description(soup),
            'images': await get_images(soup, link),
            'price': get_price(soup),
            'rooms': get_rooms(soup),
            'square': get_square(soup)
        }
        data.append(property_data)

    with open('realty_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(parse_all_data())
