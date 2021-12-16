### scraping player statuses from https://www.fplanalytics.com/playerStatus.html

import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

URL = "https://www.fplanalytics.com/playerStatus.html"

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

divs = soup.findAll('div', attrs={'class':'container'})
s = str(divs[1].find('input'))
data_url = s.split('=')[2].split(';')[0].split("'")[1]
data = requests.get(data_url)
csv_data = StringIO(data.text)
df = pd.read_csv(csv_data)
print(df.head())
