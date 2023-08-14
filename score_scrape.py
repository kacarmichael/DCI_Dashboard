#Scrape dci.org for all previous scores stored on their website

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://www.dci.org/scores'

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.content, "html.parser")

page_total = int(soup.find_all("span", class_="total")[0].text)


for page in range(1, page_total+1):

    score_url = f'{BASE_URL}?page={page}'

    response = requests.get(score_url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert len(soup.find_all("table")) == 1, "Multiple tables found"

    table = soup.find_all("table")[0]
    body = table.find_all("tbody")[0]
    events = body.find_all("tr")
    events.pop(0) #First tr is column info
    events.pop() #Last tr is sponsor info
    
    for event in events:
        event_info = event.find_all("td")
        event_name = event_info[0].text
        event_date = event_info[1].text
        event_location = event_info[2].text
        event_score_link = event_info[3].find_all("a", href=True)[0]['href']
        print(f'Event: {event_name}\nDate: {event_date}\nLocation: {event_location}\nLink: {event_score_link}')
        print("--------------------------------")
    