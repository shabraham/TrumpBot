from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import time

driver = webdriver.Firefox()
print("getting page")
#driver.get("https://twitter.com/realDonaldTrump")
driver.get("https://twitter.com/search?f=tweets&q=from%3ArealDonaldTrump%20since%3A2000-01-01%20until%3A2017-11-14&src=typd")
print("loaded page")

SCROLL_PAUSE_TIME = 2
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if (new_height == last_height):
            break
    last_height = new_height

elems = driver.find_elements_by_class_name("js-tweet-text-container")
for i in range(len(elems)):
	print(str(i) + ": " + elems[i].text +"\n")

f = open("tweets.csv", "w+")
for i in range(len(elems)):
    level = ""
    for word in elems[i].text.split(" "):
        level += (str(word) + ",")
    f.write(level[:-1] + "\n")
f.close()

print("done")
driver.close()