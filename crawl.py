import sys
import httplib2
import webbrowser
import math
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
urlArg = sys.argv[1] # sec.gov > filings > company filings search > latest filings > type '8-k' in Form Type

def getDomain(url):
    parsedUrl = urlparse(url)
    return '{uri.scheme}://{uri.netloc}'.format(uri=parsedUrl)

def getSoup(url):
    status, response = http.request(url)
    return BeautifulSoup(response)

def getLinksWithText(url, text):
    linksToReturn = []
    domain = getDomain(url)
    soup = getSoup(url)
    for tag in soup.findAll('a', href=True, text=text):
        link = tag.parent['href']
        if link[:4] != 'http':
            link = domain + link
        linksToReturn.append(link)
    return linksToReturn

def getLinksWithinTag(url, attrName, attrValue):
    linksToReturn = []
    domain = getDomain(url)
    soup = getSoup(url)
    parentElement = soup.findAll(attrs={attrName: attrValue})[0]
    links = parentElement.findAll('a')
    for link in links:
        if link.has_key('href'):
            if link['href'][:4] != 'http':
                link['href'] = domain + link['href']
            linksToReturn.append(link['href'])
    return linksToReturn

def containsOtherEvents(url):
    domain = getDomain(url)
    soup = getSoup(url)
    itemsBox = soup.find('div', {'class': 'formContent'}).text
    if itemsBox.find('Other Events') != -1:
        return True
    else:
        return False

def getFinalLinks(url):
    linksToReturn = []
    links = getLinksWithText(url, '[html]')
    for link in links:
        if containsOtherEvents(link):
            linksToReturn.append(getLinksWithinTag(link, 'class', 'tableFile')[0])
    return linksToReturn

def main():
    finalLinks = getFinalLinks(urlArg)
    for link in finalLinks:
        webbrowser.open_new_tab(link)

main()
