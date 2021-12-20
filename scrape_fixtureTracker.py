# scraping player statuses from https://allfantasytips.com/fpl-fixture-tracker/
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_player_status():
    URL = "https://allfantasytips.com/fpl-fixture-tracker/"

    # need to parse out below link from main page here
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # data link
    page = requests.get('https://playerdatabase247.com/include_premier_league_fixture_tracker_uusi.php?listtype=expgoals')
    soup = BeautifulSoup(page.content, 'html.parser')
    d = soup.find_all('td')
    dic = {}
    for x in range(7, len(soup.find_all('td')), 7):
        # get main team name
        team = re.split(r'>|<', str(d[x]))[-3]
        dic[team] = {}
        # loop through their next 5 games
        for y in range(1, 6):
            # get opponent name
            split = re.split(r'>|<', str(d[x + y]))
            if split[2] != '':
                versus = split[2].lower()
            else:
                versus = split[4].lower()
            # get xG
            score = re.findall('(\d{1}\.\d{1,2})', str(d[x + y]))[0]
            dic[team][versus] = score
        # get team total
        dic[team]['total'] = re.findall('(\d{1,2}\.\d{1,2})', str(d[x + 6]))[0]

    return dic
    # df = pd.DataFrame(dic)
    # print(df.head())
