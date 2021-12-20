# scraping player statuses from https://understat.com/league/EPL
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


def get_player_xg():
    URL = "https://understat.com/league/EPL"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    json_data = str(soup.find_all('script')[3]).split("'")[1].encode('utf8').decode('unicode_escape')

    return json_data
#     df = pd.read_json(json_data)
#     print(df.head())
# get_player_xg()