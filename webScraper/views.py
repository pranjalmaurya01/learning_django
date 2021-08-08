from django.shortcuts import redirect, render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models
import requests

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/d/services/search/bbb?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    if request.method == 'GET':
        search = request.GET['search']
        models.Search.objects.create(search=search)
        response = requests.get(BASE_CRAIGSLIST_URL.format(quote_plus(search)))
        soup = BeautifulSoup(response.text, features='html.parser')

        post_listings = soup.find_all('li', {'class': 'result-row'})
        final_postings = []

        for post in post_listings:
            post_title = post.find(class_='result-title').text[:25]
            post_url = post.find('a').get('href')

            if post.find(class_='result-price'):
                post_price = post.find(class_='result-price').text
            else:
                post_price = 'N/A'

            if post.find(class_='result-image').get('data-ids'):
                post_image_id = post.find(
                    class_='result-image').get('data-ids').split(',')[0].split(':')[1]
                post_image_url = BASE_IMAGE_URL.format(post_image_id)
            else:
                post_image_url = 'https://craigslist.org/images/peace.jpg'

            final_postings.append(
                (post_title, post_url, post_price, post_image_url))

        frontend_data = {
            'searchedData': search,
            'final_postings': final_postings
        }
        return render(request, 'new_search.html', frontend_data)

# result-row
