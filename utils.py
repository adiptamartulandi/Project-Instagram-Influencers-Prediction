import os, platform, time, urllib.request, openpyxl, operator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl import Workbook
import sys, requests, re, json
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

#Create Empty List
ranking = []
username = []
category = []
category_2 = []

def scrape_username(url):
    
    #accesing and parsing the input url
    response = requests.get(url)
    print(f'response {response}')
    soup = BeautifulSoup(response.content, 'html.parser')
    list_username = soup.find_all('tr')
    
    #looping to the element that we want to scrape
    for p in list(list_username):
        try:
            #getting the information (rank, names, and category)
            rank = p.find('td', 'align-middle').get_text().strip()
            ranking.append(rank)
            name = p.find('a').get_text().strip()
            username.append(name)
            cat = p.find_all('span', 'badge badge-pill badge-light samll text-muted')
            category_2 = []
            for c in cat:
                d = c.find('a', 'link').get_text()
                category_2.append(d)
            category.append(category_2)
        except:
            continue

    return ranking, username, category

#function to scrape general information
def scrape_general_info(url):
    # instagram URL 
    URL = url

    # creating a dictionary 
    data = {} 

    # getting the request from url 
    r = requests.get(URL)

    # converting the text 
    s = BeautifulSoup(r.text, "html.parser") 

    # finding meta info 
    meta = s.find("meta", property ="og:description")

    #searching followers, followeing and number of posts info
    meta_2 = meta.attrs['content']
    meta_3 = meta_2.split("-")[0].split(" ")

    # assigning the values 
    data['Followers'] = meta_3[0] 
    data['Following'] = meta_3[2] 
    data['Posts'] = meta_3[4]
    
    return data

#Create Empty List
link = []
names = []

def get_influencer_link(username):
    #to influencer url
    url = f'https://www.instagram.com/{username}/'
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(5)

    i = 0
    while i < 8:   
        try:
            #get the links
            pages = driver.find_elements_by_tag_name('a')
            for data in pages:
                data_2 = data.get_attribute("href")
                if '/p/' in data_2:
                    link.append(data.get_attribute("href"))
                    names.append(username)
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(1)
            i += 1
        except:
            i += 1
            continue
    driver.quit()

    return link, names


likes = []
comment_counts = []
dates = []
captions = []
type_posts = []
links = []
i = 0
n = 0

def get_information(link):    
    try:
        global i, n
        
        #accessing and parsing the website url
        url = link
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        
        #find element that contain information
        body = soup.find('body')
        script = body.find('script')
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data=json.loads(raw)
        posts =json_data['entry_data']['PostPage'][0]['graphql']
        posts= json.dumps(posts)
        posts = json.loads(posts)
        
        #acquiring information
        like = posts['shortcode_media']['edge_media_preview_like']['count']
        comment_count = posts['shortcode_media']['edge_media_to_parent_comment']['count']
        date = posts['shortcode_media']['taken_at_timestamp']
        caption = posts['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        type_post = posts['shortcode_media']['__typename']
        likes.append(like)
        comment_counts.append(comment_count)
        dates.append(date)
        captions.append(caption)
        type_posts.append(type_post)
        links.append(link)
        i += 1
    except:
        i += 1
        n += 1
        print(f'number of link error {n} at iteration {i}')
        pass
    return likes, comment_counts, dates, captions, type_posts, links