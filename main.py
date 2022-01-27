from random import randint
from warnings import warn
import requests
from requests import get
from bs4 import BeautifulSoup
import time


class CraigsPost:
    """
    This class creates a Craigslist post object with important details from the post as parameters
    """

    def __init__(self, price, time, link, heading, location):
        self._price = price
        self._time = time
        self._link = link
        self._heading = heading
        self._location = location

    def __str__(self):
        return F"Title: {self._heading}\n" \
               F"Time posted: {self._time}\n" \
               F"Price: {self._price}\n" \
               F"Location: {self._location}\n" \
               F"Link: {self._link}\n\n"


def find_cars():
    # get link with filters (craigslist adds filter options to http link)
    response = get(
        "https://vancouver.craigslist.org/search/cto?purveyor-input=owner")

    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    html_soup = BeautifulSoup(response.text, 'html.parser')

    # gets the macro-container for posts
    posts = html_soup.find_all('li', class_='result-row')
    print(type(posts))  # double checks you get a ResultSet
    print(len(posts))  # double check you get max results (120)

    for index, post in enumerate(posts):
        # returns the first result scraped
        post_one_price = post.find('span', class_='result-price')
        post_one_price_string = post_one_price.string

        # grab the time and datetime post was made
        post_one_time = post.find('time', class_='result-date')
        post_one_datetime = post_one_time['datetime']

        # grabs the link to the post
        post_one_title = post.find('a', class_='result-title hdrlnk')
        post_one_link = post_one_title['href']

        # grabs the title of the post
        post_one_title_next = post_one_title.text
        post_one_heading = post_one_title.string

        # grabs the neighborhood location of post
        post_one_location = post.find('span', class_='result-hood')
        post_one_location_string = post_one_location.string

        cg_post = CraigsPost(price=post_one_price_string, time=post_one_datetime, link=post_one_link,
                             heading=post_one_heading, location=post_one_location_string)
        with open(F"posts/{index}.txt", 'w', encoding="utf8") as f:
            f.write(cg_post.__str__())


def main():
    while True:
        find_cars()
        time_wait = randint(1, 5)
        print(F"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)


if __name__ == '__main__':
    main()
