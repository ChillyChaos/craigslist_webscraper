from requests import get
from bs4 import BeautifulSoup

# get link with filters (craigslist adds filter options to http link)
response = get(
    "https://vancouver.craigslist.org/search/cto?purveyor-input=owner")

html_soup = BeautifulSoup(response.text, 'html.parser')

# gets the macro-container for posts
posts = html_soup.find_all('li', class_='result-row')
print(type(posts))  # double checks you get a ResultSet
print(len(posts))  # double check you get max results (120)

post_one = posts[0]
# print(post_one) #just returns the first result sraped
post_one_price = post_one.a.text
post_one_price.strip()
print(post_one_price)

# grab the time and datetime post was made
post_one_time = post_one.find('time', class_='result-date')
post_one_datetime = post_one_time['datetime']
print(post_one_datetime)

# grabs the link to the post
post_one_title = post_one.find('a', class_='result-title hdrlnk')
post_one_link = post_one_title['href']
print(post_one_link)

# grabs the title of the post
post_one_title_next = post_one_title.text
post_one_heading = post_one_title.string
print(post_one_heading)

# grabs the neighborhood location of post
post_one_location = post_one.find('span', class_='result-hood')
post_one_location_string = post_one_location.string
print(post_one_location_string)