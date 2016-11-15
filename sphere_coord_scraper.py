from bs4 import BeautifulSoup
from selenium import webdriver
import re

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def extract_lat_lng(str):
    two = str.split("@")
    after_at = two[1].split(",")
    return (after_at[0], after_at[1])

def is_pano(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    active_card = soup.select(".widget-runway-card-active")
    if len(active_card) == 0:
        print("Can't find active card")

    pano_icon = active_card[0].select(".maps-sprite-photos-pano")

    return len(pano_icon) != 0

driver = webdriver.Firefox()
driver.get('https://www.google.com/maps/place/ucla')

# html = driver.page_source
# html = driver.find_element_by_class_name("section-image-pack-item-1").get_attribute('innerHTML')
# html = driver.__getattribute__(".section-image-pack-item-1")


driver.implicitly_wait(20)

clicked = driver.find_element_by_tag_name("body").find_element_by_class_name("section-image-pack-item-1").click()



try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "widget-runway-card-button"))
    )

    # widget-runway-tray-wrapper
    like = driver.find_elements_by_class_name("widget-runway-subview-card-view-container")
    left = driver.find_element_by_class_name("widget-play-left")
    right = driver.find_element_by_class_name("widget-play-right")
    print(len(like))

    like[len(like)-1].click()
    # for x in range(1, len(like)-1):
    #     print(str(x) + " " + str(len(like)))
    #     right.click()
    #     time.sleep(.5)

    time.sleep(5)

    for x in range(0, len(like)):

        active = driver.find_element_by_class_name("widget-runway-card-active")

        curr_is_pano = is_pano(driver.page_source)
        if curr_is_pano:
            coors = extract_lat_lng(driver.current_url)
            print(coors)


        # try:
        #     panos = active.find_element_by_class_name("maps-sprite-photos-pano")
        #     # print("Photo Sphere")
        #     coors = extract_lat_lng(driver.current_url)
        #     print(coors)
        # except:
        #     pass
        #     # print("Not Photo Sphere")

        right.click()
        time.sleep(1)

finally:
    print("Outer Finally")
    exit()
    driver.quit()
