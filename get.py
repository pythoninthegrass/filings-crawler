import httplib2
import webbrowser
from BeautifulSoup import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request('https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=8-k&owner=include&count=40&action=getcurrent')

all_links = BeautifulSoup(response, parseOnlyThese=SoupStrainer('a'))
html_links = []
other_events_links = []

all_buttons = BeautifulSoup(response, parseOnlyThese=SoupStrainer('button'))
next40_button = ''

for link in all_links:
    if link.has_key('href') and link['href'][:9] == '/Archives' and link['href'][-4:] == '.htm':
        html_links.append(link['href'])

for link in html_links:
    temp_status, temp_response = http.request('http://sec.gov' + link)
    soup = BeautifulSoup(temp_response, fromEncoding='utf-8')
    items_box = soup.find('div', {'class': 'formContent'}).text
    if items_box.find('Other Events') != -1:
        # find the 8-k link and use that to open the new browser tab
        temp_status2, temp_response2 = http.request('http://sec.gov' + temp_links[0])
        webbrowser.open_new_tab('http://sec.gov' + link.encode('utf-8'))
        other_events_links.append('http://sec.gov' + link.encode('utf-8'))

print other_events_links
