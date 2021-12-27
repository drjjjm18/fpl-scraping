# scraping player statuses from https://allfantasytips.com/fpl-fixture-tracker/
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def parse_stats(soup):
    d = soup.find_all('td')
    dic = {}
    for x in range(7, len(d), 7):
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
            # get xG/xCS
            score = re.findall('(\d{1}\.\d{1,2})', str(d[x + y]))[0]
            dic[team][versus] = score
        # get team total
        dic[team]['total'] = re.findall('(\d{1,2}\.\d{1,2})', str(d[x + 6]))[0]
    return dic


def get_fixture_xg():
    URL = "https://allfantasytips.com/fpl-fixture-tracker/"

    # # todo: consider parsing out xG/xCS links from main page here
    # page = requests.get(URL)
    # soup = BeautifulSoup(page.content, 'html.parser')

    # get xG stats
    page = requests.get('https://playerdatabase247.com/include_premier_league_fixture_tracker_uusi.php?listtype=expgoals')
    soup = BeautifulSoup(page.content, 'html.parser')
    xG = parse_stats(soup)

    # get xCS stats
    URL = "https://playerdatabase247.com/include_premier_league_fixture_tracker_uusi.php?listtype=cs"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    xCS = parse_stats(soup)

    return xG, xCS


# xG, xCS = get_fixture_xg()
# print(pd.DataFrame(xG).head(), pd.DataFrame(xCS).head())
