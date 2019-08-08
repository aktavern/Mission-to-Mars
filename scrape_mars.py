# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # set up path for splinter
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

     # set url and visit using splinter
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    # extract the news title and paragraph from first url
    html = browser.html
    soup = bs(html, "html.parser")

    #find the title and paragraph text from the website
    news_title = soup.find('div', class_="content_title").get_text()
    news_p = soup.find('div', class_="article_teaser_body").get_text()
    
    # set url and visit using splinter
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(1)

    html = browser.html
    img_soup = bs(html, "html.parser")

    # find background-img url and clean up url
    featured_image_url = img_soup.find('article')['style']
    cleaned_url = featured_image_url.replace('background-image: url(','').replace('(','').replace(');','')[1:-1]

    # use base url and cleaned up url to get the featured image
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + cleaned_url

    # set new url and visit twitter 
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(1)

    html = browser.html
    tweet_soup = bs(html, "html.parser")

    # select everything from the tweet section
    timeline = tweet_soup.select('#timeline div.js-actionable-tweet')

    for tweet in timeline:
        # select the tweet id 
        tweet_id = tweet['data-screen-name']
        # confirm that the correct account tweeted and get the text 
        if tweet_id == "MarsWxReport":
                tweet_text = tweet.select('p.tweet-text')[0].get_text()
                mars_weather = tweet_text
                break

    # set url for facts
    facts_url = "https://space-facts.com/mars/"

    # extract table from website using pandas
    table = pd.read_html(facts_url)

    # convert table into a dataframe
    df = pd.DataFrame(table[0])

    # convert dataframe to html 
    html_table = df.to_html()
    
    # initialize visit to astrogeology
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = bs(html, "html.parser")

    # select all product items
    products = hemi_soup.find_all('div', class_='item')

    # identify base url to be used to build out additional links
    base_url = "https://astrogeology.usgs.gov"

    hemisphere_image_urls = []

    # iterate through products to visit their urls and get image links
    for i in products:
        # collect titles and urls for enhanced images 
        titles = i.find('h3').get_text()
        url = i.find('a', class_="itemLink product-item")['href']
        # visit each url
        browser.visit(base_url + url)
        time.sleep(1)
        html = browser.html
        hemi_soup = bs(html, "html.parser")
        # get url for enhanced image
        enhanced_url = hemi_soup.find('img',class_='wide-image')['src']
        hemisphere_image_urls.append(
            {"title":titles,
            "img_url":base_url + enhanced_url}
        )

    scrape_dictionary = {}
    scrape_dictionary = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "html":html_table,
        "mars_weather": mars_weather,
        "hemisphere_images": hemisphere_image_urls
    }
    browser.quit()
    return(scrape_dictionary)
    
    
        