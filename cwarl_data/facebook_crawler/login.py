from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

browser = webdriver.Chrome(executable_path="./chromedriver")

browser.get("http://fb.me")

txtUser = browser.find_element_by_id("email")
txtUser.send_keys("dcongtinh")

txtPass = browser.find_element_by_id("pass")
txtPass.send_keys("dcongtinh")

txtPass.send_keys(Keys.ENTER)
sleep(10)

browser.close()
