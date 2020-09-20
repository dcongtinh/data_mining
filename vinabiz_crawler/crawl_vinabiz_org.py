'''
Usage:
python crawl_vinabiz_org.py -u https://vinabiz.org/categories/tinhthanh/can-tho/380031003500/ -s 1 -e 1 -o data_cwarled.csv
'''
import logging
import sys
import argparse
import urllib.parse
import requests
from bs4 import BeautifulSoup
import csv
from company import Company

cookie = '__cfduid=d3350871bb3067a286d00ce7c77fd3ef11600570776; ASP.NET_SessionId=knoqn5im1mco4oucbjuzjhdv; _ga=GA1.2.712988244.1600570779; _gid=GA1.2.593010949.1600570779; HstCfa2883594=1600570780077; HstCmu2883594=1600570780077; HstCnv2883594=1; c_ref_2883594=https%3A%2F%2Fviblo.asia%2F; HstCns2883594=2; HstCla2883594=1600573968441; HstPn2883594=18; HstPt2883594=18'
log_format = '[%(levelname)s] - %(message)s'
logging.basicConfig(level='INFO', format=log_format)
write_index = 0

parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="base url")
parser.add_argument("--start", "-s", help="start page")
parser.add_argument("--end", "-e", help="end page")
parser.add_argument("--out", "-o", help="output file")
args = parser.parse_args()

company_arr = []


def check_input():
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


def r(e, t):
    r = e[t:t+2]
    return int(r, base=16)


def decode(n, c):
    o = ''
    a = r(n, c)
    i = c + 2
    xs = i
    for x in range(i, len(n)):
        if xs in range(i, len(n)):
            l = r(n, xs) ^ a
            o += chr(l)
            xs = xs + 2
        else:
            break
    try:
        o = urllib.parse.unquote(urllib.parse.quote(o))
        return o
    except Exception as e:
        logging.error(str(e))


def request_list_company(page):
    company_url_list = []
    logging.info("getting list of company in page " + str(page))
    url = args.url
    if url[:-1] != '/':
        url = url + '/'
    if int(page) > 1:
        url = url + str(page)
    response = requests.get(url, headers={'Cookie': cookie})
    soup = BeautifulSoup(response.content, 'html.parser')
    list_of_company_div = soup.find_all(
        "div", class_="row margin-right-15 margin-left-10")
    for company_div in list_of_company_div:
        if company_div.find('a')['href']:
            company_url_list.append(company_div.find('a')['href'])
    logging.info('Get total ' + str(len(company_url_list)) + ' company url')
    return company_url_list


def parse_company_detail(rows):
    emailCode = None
    company = Company()
    company.official_name = rows[1].find_all('td')[1].get_text().strip()
    company.trading_name = rows[1].find_all('td')[3].get_text().strip()
    company.bussiness_code = rows[2].find_all('td')[1].get_text().strip()
    company.date_of_license = rows[2].find_all('td')[3].get_text().strip()
    company.start_working_date = rows[3].find_all('td')[3].get_text().strip()
    company.status = rows[4].find_all('td')[1].find_all(
        'div', class_='alert alert-success fade in')[0].get_text().strip()
    company.address = rows[7].find_all('td')[1].get_text().strip()
    company.phone = rows[8].find_all('td')[1].get_text().strip()
    if rows[9].find_all('td')[1].find('span', class_='__cf_email__'):
        emailCode = rows[9].find_all('td')[1].find(
            'span', class_='__cf_email__')['data-cfemail']
    if emailCode is not None:
        company.email = decode(emailCode, 0)
    else:
        company.email = ''
    company.director = rows[12].find_all('td')[1].get_text().strip()
    company.director_phone = rows[12].find_all('td')[1].get_text().strip()
    company.accountant = rows[14].find_all('td')[1].get_text().strip()
    company.accountant_phone = rows[14].find_all('td')[3].get_text().strip()
    return company


def get_company_details(url):
    url = 'https://vinabiz.org/' + url
    logging.info('Get company details in ' + url)
    response = requests.get(url, headers={'Cookie': cookie})
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find_all(
        "table", class_="table table-bordered")[0].find_all('tr')
    company = parse_company_detail(rows)
    if soup.find("div", {"id": "hr2"}) is not None:
        company.business_lines = soup.find("div", {"id": "hr2"}).get_text()
    else:
        company.business_lines = ''
    company_arr.append(company)


def write_sheet_header():

    sheet_header = ['Tên chính thức', 'Tên giao dịch', 'Mã doanh nghiệp', 'Ngày cấp', 'Ngày bắt đầu hoạt động',
                    'Trạng thái', 'Địa chỉ', 'Điện thoại', 'Email', 'Giám đốc', 'SĐT giám đốc',
                    'Kế toán', 'SĐT kế toán', 'Nghành nghề']
    with open(args.out, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(sheet_header)


def write_sheet_data(data):
    for company in data:
        attributes_arr = list(company.__dict__.keys())
        data_arr = []
        for att in attributes_arr:
            data_arr.append(
                str(getattr(company, att)).replace('\n', '').strip())
        with open(args.out, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data_arr)
    pass


def craw():
    total = 0
    write_sheet_header()
    company_arr.clear()
    for i in range(int(args.start), int(args.end) + 1):
        company_url_list = request_list_company(i)
        for company_url in company_url_list:
            try:
                get_company_details(company_url)
            except Exception as e:
                logging.error('url: ' + company_url)
                logging.error(str(e))
        write_sheet_data(company_arr)
        total += len(company_arr)
        company_arr.clear()
    logging.info('Get information of total ' +
                 str(len(company_arr)) + ' companies')


def main():
    check_input()
    craw()


if __name__ == "__main__":
    main()
