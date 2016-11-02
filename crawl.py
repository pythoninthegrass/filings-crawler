import sys
import httplib2
import webbrowser
import math
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
urlArg = sys.argv[1] # sec.gov > filings > company filings search > latest filings > type '8-k' in Form Type
limit = 20 # this is the limit of 8-k's you want to check for 'other events', so the number of final results will likely be smaller

def getDomain(url):
    parsedUrl = urlparse(url)
    return '{uri.scheme}://{uri.netloc}'.format(uri=parsedUrl)

def getSoup(url):
    status, response = http.request(url)
    return BeautifulSoup(response)

def getNextPageLinks(url):
    if limit <= 40:
        return
    linksToReturn = []
    domain = getDomain(url)
    soup = getSoup(url)
    iterations = math.ceil((limit - 40) / 40.0) # ensure rounding UP, by using one float so that ceil precedes int rounding
    currentUrl = url
    for i in range(iterations):
        next40Link = getLinksWithText(url, 'Next 40', 1)
        linksToReturn.append(next40Link)
        currentUrl = next40Link
    return linksToReturn

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

def getFinalLinks(url, limit):
    linksToReturn = []
    links = getLinksWithText(url, '[html]', limit)
    for link in links:
        if containsOtherEvents(link):
            linksToReturn.append(getLinksWithinTag(link, 'class', 'tableFile')[0])
    return linksToReturn

# getFinalLinks(urlArg, limit)
# for link in linksToReturn:
#     webbrowser.open_new_tab(link)

def main():
    linksToOpen = getFinalLinks(urlArg, limit)
    nextPageLinks = getNextPageLinks(urlArg)
    if nextPageLinks != None:
        for link in getNextPageLinks(urlArg):
            linksToOpen.append(getFinalLinks(link, limit))
    for link in linksToOpen:
        webbrowser.open_new_tab(link)

main()
