from bs4 import BeautifulSoup
import urllib.request
import re
import csv


def not_relative_uri(href):
    return re.compile('^https://').search(href) is not None


url = 'https://vnexpress.net'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

new_feeds = soup.find(
    'section', class_='section section_stream_home section_container').find_all(
    'a', class_='', href=not_relative_uri)

with open('data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Title', 'Link'])
    titles = {}
    for feed in new_feeds:
        if feed.get('title') not in titles:
            writer.writerow([feed.get('title'), feed.get('href')])
            titles[feed.get('title')] = feed.get('href')
