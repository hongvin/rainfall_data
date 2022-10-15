import urllib.request
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
            try:
                prev_df = pd.read_csv(f'{station_id}.csv')
            except Exception as e:
                print('Error: ',e)
            try:
                with urllib.request.urlopen(f"https://publicinfobanjir.water.gov.my/wp-content/themes/enlighten/query/getrainfalllast3dayslead.php?station={station_id}") as url:
                    data = json.load(url)
                    name = data['info']['name']
                    station_id_dict[station_id] = name
                    new_df = pd.DataFrame.from_dict(data['values'])
                    if prev_df:
                        pd.concat([prev_df,new_df]).drop_duplicates().reset_index(drop=True).to_csv(f'{station_id}.csv',index=False)
                    else:
                        new_df.to_csv(f'{station_id}.csv',index=False)
            except Exception as e:
                print('Error: ', e)
    except Exception as e:
        print('Error: ', e)

pd.DataFrame(station_id_dict.items()).to_csv('key.csv',index=False)
