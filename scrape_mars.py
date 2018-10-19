# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import fnmatch


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    # Collecting the latest News Title and Paragraph Text from NASA Mars News Site
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    # Storing the latest news title and paragraph text in variables
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    listings["news_title"] = news_soup.find('div', class_='content_title').text
    listings["news_p"] = news_soup.find('div', class_='article_teaser_body').text

    # Finding the url to featured image on NASA - Jet Propulsion Laboratory
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    # Storing the featured image URL in a variable
    browser.click_link_by_partial_text('FULL IMAGE')
    jpl_fimage_html = browser.html
    jpl_fimage_soup = BeautifulSoup(jpl_fimage_html, 'html.parser')
    article = jpl_fimage_soup.find('article',class_='carousel_item')
    dig_out_image = article["style"].split("'")
    listings["featured_image_url"] = "https://www.jpl.nasa.gov" + dig_out_image[1]

    # Finding the latest tweet on Mars Weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'html.parser')
    # Finding the twitter handle MarsWeather and storing the weather in a variable
    twitter_handles = weather_soup.find_all('a', class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")
    weather_texts = weather_soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    for index, handle in enumerate(twitter_handles):
        if fnmatch.fnmatch(handle.find('strong').text,"Mars Weather"):
            if fnmatch.fnmatch(weather_texts[index].text,"Sol*"):
                listings["mars_weather"] = weather_texts[index].text
                break

    # Scraping facts about Mars including Diameter, Mass
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['description','value']
    # Converting the df to html
    listings["facts_html"] = pd.DataFrame.to_html(df, classes="table")

    # Get images of Mars Hemispheres
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
    hems = hemi_soup.find_all('div', class_="item")
    # Getting a url for each hemisphere and visitng the page to retrieve image url and title
    hemisphere_image_urls = []
    for hem in hems:
        sublink = hem.find("a",class_="itemLink product-item")
        sub_url = "https://astrogeology.usgs.gov" + sublink["href"]
        browser.visit(sub_url)
        sub_html = browser.html
        sub_hemi_soup = BeautifulSoup(sub_html, 'html.parser')
        title = sub_hemi_soup.find("h2",class_="title").text
        img_url = "https://astrogeology.usgs.gov" + sub_hemi_soup.find("img",class_="wide-image")["src"]
        hemi_dict = {"img_url":img_url,
                 "title":title}
        hemisphere_image_urls.append(hemi_dict)    
    listings["hemi_data"] = hemisphere_image_urls

    return listings
