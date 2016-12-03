import re
import os
from xml.parsers.expat import ExpatError

import requests
import xmltodict
from py_bing_search import PyBingWebSearch

GOODREADS_API_KEY = os.environ['GOODREADS_API_KEY']
BING_SEARCH_API_KEY = os.environ['BING_SEARCH_API_KEY']


class BookNotFound(Exception):
    pass


def get_top_bing_goodreads_search(search_term):
    query = "site:goodreads.com {0}".format(search_term)
    bing_web = PyBingWebSearch(BING_SEARCH_API_KEY, query, web_only=False)
    results = bing_web.search(limit=50, format='json')
    return [r.url for r in results if 'goodreads.com/book/show/' in r.url]


def get_goodreads_id(url):
    # receives goodreads url
    # returns the id using regex
    regex = r'goodreads.com/book/show/(\d+)'
    ids = re.findall(regex, url)
    if ids:
        return ids[0]
    return False


def get_book_details_by_id(goodreads_id):
    api_url = 'http://goodreads.com/book/show/{0}?format=xml&key={1}'
    r = requests.get(api_url.format(goodreads_id, GOODREADS_API_KEY))
    try:
        book_data = xmltodict.parse(r.content)['GoodreadsResponse']['book']
    except (TypeError, KeyError, ExpatError):
        return False
    keys = ['title', 'average_rating', 'ratings_count', 'description', 'url',
            'num_pages', 'image_url']
    book = {}
    for k in keys:
        book[k] = book_data.get(k)
    try:
        work = book_data['work']
        book['publication_year'] = work['original_publication_year']['#text']
    except KeyError:
        book['publication_year'] = book_data.get('publication_year')

    if type(book_data['authors']['author']) == list:
        authors = [author['name'] for author in book_data['authors']['author']]
        authors = ', '.join(authors)
    else:
        authors = book_data['authors']['author']['name']
    book['authors'] = authors
    return book


def get_book_details_by_name(book_name):
    urls = get_top_bing_goodreads_search(search_term=book_name)
    if not urls:
        raise BookNotFound
    top_search_url = urls[0]
    goodreads_id = get_goodreads_id(url=top_search_url)
    return get_book_details_by_id(goodreads_id=goodreads_id)
