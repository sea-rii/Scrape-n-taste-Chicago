Yelp Restaurant Review Scraper

Overview
- The Yelp Restaurant Review Scraper is a Python script designed to collect restaurant data from Yelp for the Chicago area. 
- It uses the requests library to download web pages and BeautifulSoup to parse the HTML content. 
- The script collects information such as restaurant names, URLs, ratings, review counts, neighborhoods, tags, price ranges, and services, and saves this data into a CSV file.

Features
- Scrapes restaurant data from Yelp
- Extracts details such as name, image, URL, rating, review count, neighborhood, tags, price range, and services
- Handles pagination to collect data from multiple pages
- Saves the scraped data into a CSV file

Requirements
- Python 3.x
- requests library
- beautifulsoup4 library

Installation
- Clone the repository or download the script.
- Install the required Python libraries:  
  pip install requests beautifulsoup4


Code Explanation
- Initialization: Sets up the list of pages to scrape and an empty list for visited pages and scraped items.
- Scraping Loop: Loops through the pages to scrape and processes each one.
- Extracting Data: Selects and extracts restaurant data from the HTML content.
- Handling Pagination: Discovers new pagination links and adds them to the queue.
- Saving Data: Writes the scraped data to a CSV file.


