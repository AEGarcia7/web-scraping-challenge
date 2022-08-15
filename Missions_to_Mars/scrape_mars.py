#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():


    #Run DriverManager for Chrome
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Scrape the website for the news title and body
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Examine what information is necessary and where it is
    print(soup.prettify())

    #Finding the latest news title and latest news teaser body
    news_title = soup.find('div', class_='content_title').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print("--------------------------------------------------------------------")
    print(news_paragraph)

    #Scrape from site for the featured image
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Get the URl of the featured image
    image_path = soup.find_all('img')[1]["src"]
    featured_image_url = url + image_path
    featured_image_url

    #Scrape the site for information on Mars
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    html = browser.html

    # Use Pandas to get the table information about Mars
    table = pd.read_html(url)
    mars_planet_profile = table[1]
    #Change the names of the columns
    mars_planet_profile.columns = ['', 'Values']
    mars_planet_profile.set_index('', inplace = True)
    mars_planet_profile

    # Use Pandas to convert the data to a HTML table string.
    mars_planet_profile.to_html('table.html')

    #Scrape the site to find high-resolution images for each hemisphere of Mars.
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Save the image URL string for the full res hemisphere image and the hemisphere title containing the hemisphere name. 
    #Use a Python dictionary to store the data using the keys img_url and title.
    hemisphere_image_urls=[]
    products = soup.find ('div', class_='result-list')
    hemispheres = products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup=BeautifulSoup(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    hemisphere_image_urls

    browser.quit()

    return hemisphere_image_urls