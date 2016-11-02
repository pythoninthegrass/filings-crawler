import sys
import httplib2
import webbrowser
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
urlArg = sys.argv[1]
limit = 20 # this is the limit of 8-k's you want to check for 'other events', so the number of final results will likely be less than this number
# https://www.sec.gov/cgi-bin/current?q1=0&q2=4&q3=

def getDomain(url):
    parsedUrl = urlparse(url)
    return '{uri.scheme}://{uri.netloc}'.format(uri=parsedUrl)

def getSoup(url):
    status, response = http.request(url)
    return BeautifulSoup(response)

def getLinksWithText(url, text, limit):
    linksToReturn = []
    counter = 0
    domain = getDomain(url)
    soup = getSoup(url)
    for tag in soup.findAll('a', href=True, text=text):
        if counter < limit:
            link = tag.parent['href']
            if link[:4] != 'http':
                link = domain + link
            linksToReturn.append(link)
            counter += 1
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

def main(url, limit):
    linksToOpen = []
    links = getLinksWithText(url, '8-K', limit)
    for link in links:
        if containsOtherEvents(link):
            print getLinksWithinTag(link, 'class', 'tableFile')[0]
            linksToOpen.append(getLinksWithinTag(link, 'class', 'tableFile')[0])
    for link in linksToOpen:
        webbrowser.open_new_tab(link)


main(urlArg, limit)
# webbrowser.open_new_tab('http://sec.gov' + link.encode('utf-8'))





# filingLinks = getLinksWithText(urlArg, '8-K')
# getLinksWithinTag(urlArg, 'class', 'tableFile')
