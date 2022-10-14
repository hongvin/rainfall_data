import urllib
from bs4 import BeautifulSoup
import ssl
import json
import pandas as pd
from datetime import date

ssl._create_default_https_context = ssl._create_unverified_context
today_date = date.today().strftime("%d/%m/%Y")
states = ['PLS','KDH','PNG','PRK','SEL','WLH','PTJ','NSN','MLK','JHR','PHG','TRG','KEL','SRK','SAB','WLP']

station_id_dict = {}

for state in states:
    print('States: ',state)
    try:
        url = f'https://publicinfobanjir.water.gov.my/wp-content/themes/shapely/agency/searchresultrainfall.php?state={state}&district=ALL&station=ALL&loginStatus=0&language=1'
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
        for link in soup.find('table').find_all('a', href=True):
            station_id = link['href'].split('=')[1]
            print('Station ID: ', station_id)
            with urllib.request.urlopen(f"https://publicinfobanjir.water.gov.my/wp-content/themes/enlighten/query/searchresultrainfalldthourlylead.php?extra=&station=6502010_&from=01/01/2018%2000:00&to={today_date}%2000:00&datafreq=15") as url:
                data = json.load(url)
                name = data['info']['name']
                station_id_dict[station_id] = name
                pd.DataFrame.from_dict(data['values']).to_csv(f'{station_id}.csv',index=False)
    except Exception as e:
        print('Error: ', e)

pd.DataFrame(station_id_dict.items()).to_csv('key.csv',index=False)
