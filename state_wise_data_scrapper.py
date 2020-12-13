import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json


def scrape_state_wise_date(urls):
    req = Request(urls,headers={'User-Agent': 'Mozilla/5.0'})
    
    url = urlopen(req).read()

    soup = BeautifulSoup(url, 'html.parser')

    corona_statewise_data = soup.select('#tablepress-96 > tbody > tr')
     
    state_wise_data = []

    corona_statewise_totaldata = soup.select('#tablepress-96 > tfoot > tr ')

    print(corona_statewise_totaldata)

    info = {
                "Total number of confirmed cases in India" : str(corona_statewise_totaldata[-1].select('th')[1].text),
                "Total number of deaths  in India"    : str(corona_statewise_totaldata[-1].select('th')[3].text),
                "Total number of recovered  in India" : str(corona_statewise_totaldata[-1].select('th')[2].text)
            }

    state_wise_data.append(info)        

    print(state_wise_data) 
    for corona_statewise_data in corona_statewise_data:
        info = {
            "state": str(corona_statewise_data.find_all('td')[0].text),
            "confirmed" : str(corona_statewise_data.find_all('td')[1].text),
            "recovered"    : str(corona_statewise_data.find_all('td')[2].text),
            "deaths" : str(corona_statewise_data.find_all('td')[3].text)
            }
        state_wise_data.append(info)

    print(state_wise_data)    
   
    data = {}
    data['state_wise_data'] = state_wise_data
    with open('state_wise_data.json', 'w') as outfile:
        json.dump(data, outfile,indent=4)
   





 










 




