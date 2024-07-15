import requests
from bs4 import BeautifulSoup
import csv

visited_pages = []

pages_to_scrape = ['https://www.yelp.com/search?find_desc=Restaurants&find_loc=Chicago%2C+IL']

# to store the scraped data
items = []

# to avoid overwhelming Yelp's servers with requests
limit = 7
i = 0

while len(pages_to_scrape) != 0 and i < limit:

    # extract the first page from the array
    url = pages_to_scrape.pop(0)

    # mark it as "visited"
    visited_pages.append(url)

    # download and parse the page
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # select all item card
    html_item_cards = soup.select('[data-testid="serp-ia-card"]')

    for html_item_card in html_item_cards:

        # scraping logic
        item = {}

        image = html_item_card.select_one('[data-lcp-target-id="SCROLLABLE_PHOTO_BOX"] img').attrs['src']

        name = html_item_card.select_one('h3 a').text

        url = 'https://www.yelp.com' + html_item_card.select_one('h3 a').attrs['href']

        #html_rating_element = html_item_card.select_one('[class^="y-css-ohs7lg"]')

        #rating = html_rating_element.select_one('[class^="y-css-jf9frv"]')  #.replace(' star rating', '')
        #rating = all.find('div', {'aria-label': re.compile(' star rating')})['aria-label']
        rating = soup.find("div",{"class":"y-css-9tnml4"}).get('aria-label')

        #reviews = all.find_all('span', {'class': 'css-bq71j2'}).text
        reviews = soup.find_all("span", {"class":"y-css-wfbtsu"})[0].text

        #reviews = html_item_card.sel

        neigh = soup.find_all("span", {"class":"y-css-wfbtsu"})[1].text

        tags = []

        html_tag_elements = html_item_card.select('[class^="priceCategory"] button')

        for html_tag_element in html_tag_elements:
            tag = html_tag_element.text
            tags.append(tag)

        price_range_html = html_item_card.select_one('[class^="priceRange"]')

        # this HTML element is optional
        if price_range_html is not None:
            price_range = price_range_html.text


        services = []

        html_service_elements = html_item_card.select('[data-testid="TRUSTED_PROPERTY"] div[class^=""]')

        for html_service_element in html_service_elements:
            service = html_service_element.text
            services.append(service)


        # add the scraped data to the object

        # and then the object to the array

        item['Name'] = name

        item['Image'] = image

        item['URL'] = url

        item['Rating'] = rating

        item['Review Count'] = reviews

        item['Neighbourhood'] = neigh

        item['Tags'] = tags

        item['Price Range'] = price_range

        item['Services'] = services

        items.append(item)

    #print(item)


    # discover new pagination pages and add them to the queue

    pagination_link_elements = soup.select('[class^="pagination-links"] a')

    for pagination_link_element in pagination_link_elements:
        pagination_url = pagination_link_element.attrs['href']

        # if the discovered URL is new
        if pagination_url not in visited_pages and pagination_url not in pages_to_scrape:
            pages_to_scrape.append(pagination_url)

    # increment the page counter
    i += 1

# extract the keys from the first object in the array

# to use them as headers of the CSV

headers = items[0].keys()

# initialize the .csv output file

with open('restaurants.csv', 'w', newline='', encoding='utf-8') as csv_file:

    writer = csv.DictWriter(csv_file, fieldnames=headers, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    # populate the CSV file
    for item in items:
        # transform array fields from "['element1', 'element2', ...]"

        # to "element1; element2; ..."

        csv_item = {}

        for key, value in item.items():
            if isinstance(value, list):
                csv_item[key] = '; '.join(str(e) for e in value)
            else:
                csv_item[key] = value

        # add a new record
        writer.writerow(csv_item)
        
