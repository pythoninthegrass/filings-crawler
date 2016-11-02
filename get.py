import httplib2
import webbrowser
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()

def get_links_from_page(url):
    links_to_return = []
    parsed_url = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)
    status, response = http.request(url)
    all_links = BeautifulSoup(response, parseOnlyThese=SoupStrainer('a'))
    for link in all_links:
        if link.has_key('href'):
            if link['href'][:4] != 'http':
                link['href'] = domain + link['href']
            links_to_return.append(link['href'])
    return links_to_return

def get_links_within_tag(url, attr_name, attr_value):
    links_to_return = []
    parsed_url = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)
    status, response = http.request(url)
    soup = BeautifulSoup(response)
    parent_element = soup.findAll(attrs={attr_name: attr_value})[0]
    links = parent_element.findAll('a')
    for link in links:
        if link.has_key('href'):
            if link['href'][:4] != 'http':
                link['href'] = domain + link['href']
            links_to_return.append(link['href'])
    return linksToReturn

def filter_links_that_start_with(links, string):
    links_to_return = []
    length = len(string)
    for link in links:
        if link[:length] == string:
            links_to_return.append(link)
    return links_to_return

def filter_links_that_end_with(links, string):
    links_to_return = []
    length = len(string)
    for link in links:
        if link[-length:] == string:
            links_to_return.append(link)
    return links_to_return

status, response = http.request('https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=8-k&owner=include&count=40&action=getcurrent')
all_links = BeautifulSoup(response, parseOnlyThese=SoupStrainer('a'))
print type(all_links)

# all_links = BeautifulSoup(response, parseOnlyThese=SoupStrainer('a'))
# html_links = []
# other_events_links = []
#
# # for next page
# all_buttons = BeautifulSoup(response, parseOnlyThese=SoupStrainer('button'))
# next40_button = ''
#
# for link in all_links:
#     if link.has_key('href') and link['href'][:9] == '/Archives' and link['href'][-4:] == '.htm':
#         html_links.append(link['href'])
#
# for link in html_links:
#     temp_status, temp_response = http.request('http://sec.gov' + link)
#     soup = BeautifulSoup(temp_response, fromEncoding='utf-8')
#     items_box = soup.find('div', {'class': 'formContent'}).text
#     if items_box.find('Other Events') != -1:
#         webbrowser.open_new_tab('http://sec.gov' + link.encode('utf-8'))
