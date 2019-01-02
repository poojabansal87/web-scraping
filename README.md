## web-scraping
### Web Scraping and Mongo homework

## Background

The aim of the project is to build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. 

## Step 1 - Scraping

* Jupyter Notebook file called `mission_to_mars.ipynb` contains the code for all of the scraping and analysis tasks. The following outlines what was scraped.

### NASA Mars News

* Scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text.

### JPL Mars Space Images - Featured Image

* Used splinter to navigate the site [JPL Featured Space Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.

### Mars Weather

* Scrape the latest Mars weather tweet from the page [Mars Weather twitter account](https://twitter.com/marswxreport?lang=en). Saved the tweet text for the weather report as a variable called `mars_weather`.

### Mars Facts

* Used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. from the [Mars Facts webpage](http://space-facts.com/mars/). 

* Used Pandas to convert the data to a HTML table string.

### Mars Hemispheres

* Obtain high resolution images from [USGS Astrogeology site](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) for each of Mar's hemispheres.

* Used a Python dictionary to store the data using the keys `img_url` and `title`.

* Created a list with the dictionary containing the image url string and the hemisphere title, one for each hemisphere.

## Step 2 - MongoDB and Flask Application

Used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* Converted Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of scraping code from above and return one Python dictionary containing all of the scraped data.

* Created a route called `/scrape` that will import `scrape_mars.py` script and call `scrape` function.

  * Store the return value in Mongo as a Python dictionary.

* Created a root route `/` that will query Mongo database and pass the mars data into an HTML template to display the data.

* Created a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements.
- - -

## Specifics

* Used Splinter to navigate the sites when needed and BeautifulSoup to help find and parse out the necessary data.

* Used Pymongo for CRUD applications for database. For this project, simply overwrite the existing document each time the `/scrape` url is visited and new data is obtained.

* Used Bootstrap to structure HTML template.
