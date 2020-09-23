'''
Usage: python Facebook_B1709632.py
Crawl comment from a PUBLIC post on facebook
'''
from selenium import webdriver
from time import sleep
import random
import csv

# 1. Khai báo browser
browser = webdriver.Chrome(executable_path="./chromedriver")

# 2. Mở URL của post
browser.get("https://www.facebook.com/daa.ctu.edu.vn/posts/3223134181068646")

sleep(random.randint(4, 6))

skip_login = browser.find_element_by_xpath(
    "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[4]/a")
skip_login.click()

sleep(random.randint(3, 7))

# 3. Lấy link hiện comment
showcomment_link = browser.find_element_by_xpath(
    "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/div/div[2]/div[1]/div/div[3]/span[1]/a")
showcomment_link.click()
sleep(random.randint(3, 4))

# 4. Lấy comment
showmore_link = browser.find_element_by_xpath(
    "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/form/div/div[3]/div[1]/div[1]/a")

for i in range(6):
    showmore_link.click()
    sleep(random.randint(4, 6))

# 5. Tìm tất cả các comment và ghi ra màn hình (hoặc file)
# -> lấy all thẻ div có thuộc tính aria-label='Bình luận'

comment_list = browser.find_elements_by_xpath("//div[@aria-label='Bình luận']")

# Lặp trong tất cả các comment và hiển thị nội dung comment ra màn hình
filename = "comments_list.csv"
with open(filename, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["fullname", "link_fb", "comment"])

cnt = 0
for comment in comment_list:
    # hiển thị tên, link fb và comment cấp 1
    poster = comment.find_element_by_class_name("_6qw4")
    try:
        # Comment có thể chỉ là hình ảnh
        # Nên không có element class "_3l3x"
        content = comment.find_element_by_class_name("_3l3x")
        comment = content.text.strip().replace(
            '\n', '').replace('\t', '') if content else ''
    except:
        comment = ''
    fullname = poster.text
    link_cmt = poster.get_attribute("href")
    # Lấy từ '?' trở về trước trong link comment
    link_fb = link_cmt[:link_cmt.find('?')] if link_cmt else ''
    arr = [fullname, link_fb, comment]
    print("*", fullname, "-", link_fb, ":", comment)
    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(arr)
    cnt += 1

print("\n%d comments were crawled.\n" % cnt)

sleep(2)

# 6. Đóng browser
browser.close()
