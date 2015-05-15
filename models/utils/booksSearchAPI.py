# coding: utf-8
import requests
from bs4 import BeautifulSoup
from views.templates.JSONResponse import JSONResponse


url_search_base = 'http://search.books.com.tw/exep/prod_search.php?key='

def getProductLink(ISBN):
    print('Getting ' + url_search_base+ISBN)
    response = requests.get(url_search_base+ISBN)
    response.encoding = 'utf-8'
    HTML = response.text
    soup = BeautifulSoup(HTML)

    for link in soup.find_all('a'):
        if link.get('href').__contains__('mid&'):
            booklink = link

    return booklink.get('href')

def getProductInfoHTML(link):
    response = requests.get(link)
    response.encoding = 'utf-8'
    return response.text

def getProductInfoStr(HTML):
    soup = BeautifulSoup(HTML)
    for s in soup.find_all('meta'):
        print(s['content'])
        if s['content'].__contains__(u'書名'):
            result = s['content']
    return result

def getProductInfoPic(HTML):
    soup = BeautifulSoup(HTML)
    for s in soup.find_all('meta'):
        print(s['content'])
        if s['content'].__contains__(u'getImage'):
            result = s['content']
    return result

def getProductInfoByISBN(ISBN):
    resultdict = dict()
    HTML = getProductInfoHTML(getProductLink(ISBN))
    info = getProductInfoStr(HTML).encode('utf-8')
    pic = getProductInfoPic(HTML).encode('utf-8')
    for s in info.split('，'):
        try:
            tmp = s.split('：')
            resultdict[tmp[0]] = tmp[1]
        except Exception:
            pass
    resultdict['cover_image_url'] = pic
    return JSONResponse(resultdict)