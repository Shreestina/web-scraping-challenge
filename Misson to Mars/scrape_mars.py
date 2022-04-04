from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# DB Setup
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)

#db = client.mars_db
#collection = db.items

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
#mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
     

    # Initialize browser 
    browser = init_browser()

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')  

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div',class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    # Display scrapped data 
    print("This is the title:", news_title)
    print("Summary:", news_p)

    #Mars Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(url)

    image_url = "https://www.jpl.nasa.gov/images?query=&page=1&topics=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #print(soup.prettify())

    images=soup.find_all('img', class_="BaseImage object-contain")

    # pull image link
    pic_src = []
    for image in images:
        pic = image['data-src']
    
    featured_image_url = pic
    print("featured_image_url:",featured_image_url)

    #Mars Facts
    facts_url = 'https://galaxyfacts-mars.com'

    browser.visit(facts_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)
    mars_facts

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[1]

    # Display mars_df
    mars_df

    # Save html code to folder Assets
    new_df=mars_df.to_html(header=True)

    #Mars Hemisphere
    # 1
    hem_url= 'https://marshemispheres.com/'
    browser.visit(hem_url)
    # HTML Object
    html_hem = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hem, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://marshemispheres.com/'

    # Loop through the items previously stored
    for i in items:
        # Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    # Display hemisphere_image_urls
    hemisphere_image_urls

    # Return results
    
    mars_data ={
		'news_title' : news_title,
		'news_p': news_p,
        'img_url': featured_image_url,
		'mars_df' : new_df,
		'hemisphere_image_urls': hemisphere_image_urls,
        'url': url,
        'facts_url': facts_url,
        'hemispheres_main_url': hemispheres_main_url,
        }

    browser.quit()

    print(mars_data)

    return mars_data
    

scrape_mars_news()
    
