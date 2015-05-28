# coding: utf-8
import requests
from bs4 import BeautifulSoup
from views.templates.JSONResponse import JSONResponse


search_base_url = 'http://search.books.com.tw/exep/prod_search.php?sort=1&key='
book_search_base_url = 'http://search.books.com.tw/exep/prod_search.php?sort=1&cat=1&key='

def getProductLink(ISBN):
    response = requests.get(search_base_url+ISBN)
    response.encoding = 'utf-8'
    HTML = response.text
    soup = BeautifulSoup(HTML)

    for link in soup.find_all('a'):
        if link.get('href').__contains__('mid&'):
            booklink = link

    return booklink.get('href')


def getProductLinksList(bookname):
    response = requests.get(book_search_base_url+bookname)
    response.encoding = 'utf-8'
    HTML = response.text
    soup = BeautifulSoup(HTML)
    resultlist = list()

    for link in soup.find_all('a'):
        if link.get('href').__contains__('mid&'):
            resultlist.append(link.get('href'))

    return resultlist


def getHTMLByLink(link):
    response = requests.get(link)
    response.encoding = 'utf-8'
    return response.text

def getBookname(HTML):
    soup = BeautifulSoup(HTML)
    for s in soup.find_all('meta'):
        if s.get('name') == 'keywords':
            result = s['content']
    return result


def getProductInfoStr(HTML):
    soup = BeautifulSoup(HTML)
    for s in soup.find_all('meta'):
        if s['content'].__contains__(u'書名'):
            result = s['content']
    return result


def getProductInfoPic(HTML):
    soup = BeautifulSoup(HTML)
    for s in soup.find_all('meta'):
        if s['content'].__contains__('getImage'):
            result = s['content']
    return result


def getProductInfoByISBN(ISBN):
    resultdict = dict()
    HTML = getHTMLByLink(getProductLink(ISBN))
    info = getProductInfoStr(HTML).encode('utf-8')
    pic = getProductInfoPic(HTML).encode('utf-8')
    bookname = getBookname(HTML).encode('utf-8')
    for s in info.split('，'):
        try:
            tmp = s.split('：')
            if tmp[0] == '譯者':
                resultdict['translater'] = tmp[1]
            elif tmp[0] == 'ISBN':
                resultdict['ISBN'] = tmp[1]
            elif tmp[0] == '原文名稱':
                resultdict['original_bookname'] = tmp[1]
            elif tmp[0] == '類別':
                resultdict['category'] = tmp[1]
            elif tmp[0] == '語言':
                resultdict['language'] = tmp[1]
            elif tmp[0] == '作者':
                resultdict['author'] = tmp[1]
            elif tmp[0] == '出版社':
                resultdict['publisher'] = tmp[1]
            elif tmp[0] == '頁數':
                resultdict['pages'] = tmp[1]
            elif tmp[0] == '出版日期':
                resultdict['publish_date'] = tmp[1].replace('/', '')
            # resultdict[tmp[0]] = tmp[1]
        except Exception:
            pass
    resultdict['bookname'] = bookname
    resultdict['cover_image_url'] = pic
    return JSONResponse(resultdict)


def removeTwiceDuplicated(List):
    resultlist = list()
    count = List.__len__()
    for i in range(0, count-1, 2):
        resultlist.append(List[i])
    return resultlist


def searchProductInfoListByBookname(bookname):
    resultlist = list()
    for link in removeTwiceDuplicated(getProductLinksList(bookname)):
        resultdict = dict()
        HTML = getHTMLByLink(link)
        info = getProductInfoStr(HTML).encode('utf-8')
        pic = getProductInfoPic(HTML).encode('utf-8')
        for s in info.split('，'):
            try:
                tmp = s.split('：')
                if tmp[0] == '譯者':
                    resultdict['translater'] = tmp[1]
                elif tmp[0] == 'ISBN':
                    resultdict['ISBN'] = tmp[1]
                elif tmp[0] == '原文名稱':
                    resultdict['original_bookname'] = tmp[1]
                elif tmp[0] == '類別':
                    resultdict['category'] = tmp[1]
                elif tmp[0] == '語言':
                    resultdict['language'] = tmp[1]
                elif tmp[0] == '作者':
                    resultdict['author'] = tmp[1]
                elif tmp[0] == '出版社':
                    resultdict['publisher'] = tmp[1]
                elif tmp[0] == '書名':
                    resultdict['bookname'] = tmp[1]
                elif tmp[0] == '頁數':
                    resultdict['pages'] = tmp[1]
                elif tmp[0] == '出版日期':
                    resultdict['publish_date'] = tmp[1]
                #resultdict[tmp[0]] = tmp[1]
            except Exception:
                pass
        resultdict['cover_image_url'] = pic
        resultlist.append(resultdict)

    return JSONResponse(resultlist)
