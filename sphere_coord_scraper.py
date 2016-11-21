from bs4 import BeautifulSoup
from selenium import webdriver
import re
import sys
import cssutils



from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

def get_thumbnail_url(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    active_card = soup.select(".widget-runway-card-active")
    if len(active_card) == 0:
        print("Can't find active card")

    img = active_card[0].select(".widget-runway-card-background-flicker-hack")
    thumbnail_url = img[0]['src'][2:]

    return "http://" + thumbnail_url

def get_uploader(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    div_imgs = soup.select(".widget-titlecard-attribution-image")

    div_style = div_imgs[-1]['style']

    style = cssutils.parseStyle(div_style)
    uploader_photo_url = "http://" + style['background-image'][6:]

    span_name = soup.select(".widget-titlecard-attribution-text")[-1]
    uploader_name = span_name.text

    uploader = dict()
    uploader['photo_url'] = uploader_photo_url
    uploader['name'] = uploader_name

    return uploader


def extract_photo_spheres(school, driver):


    spheres = []
    time.sleep(5)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "section-image-pack-item-1"))
    )
    time.sleep(5)

    clicked = driver.find_element_by_tag_name("body").find_element_by_class_name("section-image-pack-item-1").click()

# try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "widget-runway-card-button"))
    )

    # widget-runway-tray-wrapper
    like = driver.find_elements_by_class_name("widget-runway-subview-card-view-container")
    left = driver.find_element_by_class_name("widget-play-left")
    right = driver.find_element_by_class_name("widget-play-right")
    print(len(like))

    like[len(like) - 1].click()
    # for x in range(1, len(like)-1):
    #     print(str(x) + " " + str(len(like)))
    #     right.click()
    #     time.sleep(.5)

    time.sleep(5)

    # click the 3rd one to start with, first two are just normal images
    like[2].click()

    for x in range(0, 5):
    # for x in range(0, len(like)):

        active = driver.find_element_by_class_name("widget-runway-card-active")

        curr_is_pano = is_pano(driver.page_source)
        if curr_is_pano:
            sphere = dict()
            coors = extract_lat_lng(driver.current_url)

            thumbnail_url = get_thumbnail_url(driver.page_source)
            uploader = get_uploader(driver.page_source)

            sphere['uploader'] = uploader
            sphere['school_name'] = school
            sphere['lat'] = coors[0]
            sphere['lng'] = coors[1]
            sphere['thumbnail_url'] = thumbnail_url

            spheres.append(sphere)
            print(thumbnail_url)
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
# except:
    print("Unexpected error:", sys.exc_info()[0])

# finally:
    print("Outer Finally: "+ school)
    driver.quit()
    return spheres


def scrape(school):
    driver = webdriver.Firefox()
    driver.get('https://www.google.com/maps')

    search_box = driver.find_element_by_id("searchboxinput")
    search_box.send_keys(school)
    search_box.send_keys(Keys.ENTER)

    schools_photo_spheres = extract_photo_spheres(school, driver)
    return schools_photo_spheres

