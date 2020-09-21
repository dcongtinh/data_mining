'''
Usage:
python WineEnthusiast_B1709632.py -u https://www.winemag.com/?s=&drink_type=wine -s 1 -e 1 -o data_cwarled.csv
'''
import logging
import sys
import argparse
import urllib.parse
import requests
from bs4 import BeautifulSoup, NavigableString
import csv

log_format = '[%(levelname)s] - %(message)s'
logging.basicConfig(level='INFO', format=log_format)

parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="base url")
parser.add_argument("--start", "-s", help="start page")
parser.add_argument("--end", "-e", help="end page")
parser.add_argument("--out", "-o", help="output file")
args = parser.parse_args()

if args.url is None:
    logging.error('Please enter base url')
    sys.exit(0)
if args.start is None:
    logging.error('Please enter start page')
if int(args.start) <= 0:
    logging.error('Please enter start page > 0')
    sys.exit(0)
if args.end is None:
    logging.error('Please enter end page')
    sys.exit(0)
if int(args.start) > int(args.end):
    logging.error('Please enter start page < end page')
    sys.exit(0)
if args.out is None:
    logging.error('Please enter output file')
    sys.exit(0)


def request_list_attribute(page):
    attribute_url_list = []
    logging.info("getting list of attribute in page " + str(page))
    url = args.url + '?page=' + str(page)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, 'html.parser')
    review_list = soup.find_all(
        "li", class_="review-item")
    for attribute_div in review_list:
        if attribute_div.find('a')['href']:
            attribute_url_list.append(attribute_div.find('a')['href'])
    logging.info('Get total ' + str(len(attribute_url_list)) +
                 ' attribute url')
    return attribute_url_list


def get_text_ONLY(el):
    return [element for element in el if isinstance(
        element, NavigableString)][0].strip()


def get_attribute_details(url):
    title = variety = winery = points = price = designation = description = ''
    country = province = region_1 = region_2 = taster_name = taster_twitter_handle = ''
    logging.info('Get attribute details in ' + url)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, 'html.parser')

    description = soup.find_all("p", {"class": "description"})[0]
    description = get_text_ONLY(description)

    title = soup.find_all("div", {"class": "article-title"})[0].find("h1")
    title = get_text_ONLY(title)

    points = soup.find("span", {"class": "rating"})
    points = get_text_ONLY(points)

    div_info = soup.find_all(
        "ul", {"class": "primary-info"})[0].find_all("div", {"class": "info medium-9 columns"})

    price = get_text_ONLY(div_info[0].find("span").find("span"))[
        1:-1]  # remove '$', ','
    designation = get_text_ONLY(div_info[1].find("span").find("span"))
    variety = get_text_ONLY(div_info[2].find("span").find("a"))
    address = div_info[3].find("span").find_all("a")

    address_idx = len(address)-1
    if address_idx >= 0:
        country = get_text_ONLY(address[address_idx])
        address_idx -= 1
    if address_idx >= 0:
        province = get_text_ONLY(address[address_idx])
        address_idx -= 1
    if address_idx == 1:
        region_1 = get_text_ONLY(address[0])
        region_2 = get_text_ONLY(address[1])
    elif address_idx == 0:
        region_1 = get_text_ONLY(address[0])

    winery = get_text_ONLY(div_info[4].find("span").find("span").find("a"))
    taster_name_el = soup.find("span", {"class": "taster-area"}).find("a")
    taster_name = get_text_ONLY(taster_name_el)
    twitter_url = taster_name_el["href"]

    response = requests.get(twitter_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, 'html.parser')
    taster_twitter_handle = soup.find("li", "info-item twitter").find("a")
    taster_twitter_handle = get_text_ONLY(taster_twitter_handle)
    attribute_arr = [country, description, designation, points, price, province,
                     region_1, region_2, taster_name, taster_twitter_handle, title, variety, winery]
    return attribute_arr


def write_header():
    header = ['country', 'description', 'designation', 'points', 'price', 'province',
              'region_1', 'region_2', 'taster_name', 'taster_twitter_handle', 'title', 'variety', 'winery']
    with open(args.out, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)


def write_data(data):
    with open(args.out, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)
    pass


total = 0
write_header()
for i in range(int(args.start), int(args.end) + 1):
    urls = request_list_attribute(i)
    for url in urls:
        try:
            attribute_arr = get_attribute_details(url)
            write_data(attribute_arr)
            total += 1
        except Exception as e:
            logging.error('url: ' + url)
            logging.error(str(e))

logging.info('Get information of total ' +
             str(total) + ' wines')
