import requests
from brokest import queue

def count_words_in_page(url):
    resp = requests.get(url)
    return len(resp.text.split())

print queue(count_words_in_page, 'http://www.jeffknupp.com')
print queue(count_words_in_page, 'http://www.yahoo.com')
