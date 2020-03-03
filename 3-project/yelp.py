from bs4 import BeautifulSoup

def wine_bar_yelp(idx):
    start = idx*20 + 1 
    url = f'https://www.yelp.com/biz/maxs-wine-dive-dallas/review_feed/?start={start}&sort_by=date_desc'
    import requests
    response = requests.get(url)
    return response.json()['review_list']

def parse_reviews(response_list):
    soup = BeautifulSoup(response_list, 'lxml')
    return soup.find_all('div', {"class": "review-content"})

def extract_text(review_html):
    return review_html.find('p').text

def extract_rating(review_html):
    return float(review_html.find('div', {'class': 'rating-large'}).attrs['title'][0:3])

def extract_date(review):
    review_text = review.find('span', {'class': 'rating-qualifier'}).text
    import re
    regex = '\d{1,2}\/\d{1,2}\/\d{4}'
    m = re.search(regex, review_text)
    return m.group(0)

def extract_reviews(reviews_html):
    reviews = []
    for review_html in reviews_html:
        review = {
        'rating': extract_rating(review_html),
        'date': extract_date(review_html),
        'text': extract_text(review_html)
    }
        reviews.append(review)
    return reviews