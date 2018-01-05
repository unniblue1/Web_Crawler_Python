from bs4 import BeautifulSoup
from urllib.request import urlopen
from html.parser import HTMLParser
import re
import urllib.request
import requests
import queue
import pdb
import ssl
import os


if __name__ == '__main__':
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    q = queue.Queue(maxsize=0)
    initialurls = ['https://en.wikipedia.org/wiki/Mahatma_Gandhi', 'https://en.wikipedia.org/wiki/Indian_independence_movement']
    relatedterms = ['Annie Besant', 'Congress', 'Indira Gandhi', 'Quit India', '1947', 'bhagat', 'World', 'War', 'India', 'Independence']
    visitedurls = []
    count = 0
    for url in initialurls:
        q.put(url)
    while not q.empty ():
        f = open(r'C:\Users\user\Desktop\Information Retrieval\Assignment 2 -Web Crawler\wiki.txt', mode='at', encoding = 'utf-8')
        link = q.get()
        visitedurls.append(link)
        html = get_html(link)
        text = get_html_text(html)
        n = 0
        for term in relatedterms:
            if term in text:
                n = n+1
                if (n>=2):
                    break
        if (n>=2):
            print (link)
            f.write (link)
            f.write('\n')
            write_content_to_file(text,count)
            count = count + 1
            if (count >= 500):
                break
        urls = get_urls(html)
        for url in urls:
            if (url not in visitedurls and is_url_valid(url)):
                newformatedurl = reformat_url(url)
                q.put(newformatedurl)
    f.close()

def get_html_text(html):
    soup = BeautifulSoup(html,'html.parser')
    text = soup.get_text()
    # text = requests.get(url).text
    # print('text', text)
    return text


def get_html(url):
    try:
        response = urlopen(url).read()
        return response
    except Exception as e:
        print(e)
        return None


def get_urls(html):
    soup = BeautifulSoup(html,'html.parser')
    links = soup.find_all('a')
    urls=[]
    for link in links:
        urls.append(link.get('href'))
    return urls

def write_content_to_file(webPageContent, count):
    # url = 'https://en.wikipedia.org/wiki/Mahatma_Gandhi'
    filename = "webpage" + str(count)
    formattedhtmltext = webPageContent.strip()
    filepath = os.path.join(r'C:\Users\user\Desktop\Information Retrieval\Assignment 2 -Web Crawler\Webcrawlerstuff\htmlpages', filename)
    if not os.path.exists(r'C:\Users\user\Desktop\Information Retrieval\Assignment 2 -Web Crawler\Webcrawlerstuff\htmlpages'):
        os.makedirs(r'C:\Users\user\Desktop\Information Retrieval\Assignment 2 -Web Crawler\Webcrawlerstuff\htmlpages')
    f = open(filepath, 'a', encoding = 'utf-8')
    f.write(formattedhtmltext)
    f.close()


def is_url_valid(url):
    if url is None:
        return False
    match=re.match('^/wiki/',url)
    if match is not None:
        return True
    else:
        return False


def reformat_url(url):
    match=re.search('^/wiki/',url)
    if match:
        return "https://en.wikipedia.org"+url
    else:
        return url