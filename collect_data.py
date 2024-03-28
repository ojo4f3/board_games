import re
import json

import requests
import pandas as pd
from bs4 import BeautifulSoup


class CollectBoardGameException(Exception):
    pass


def collect_data(game_id: str) -> tuple[list, list]:
    """
    Collect board game data for a given board game ID and returns the data as a tuple of lists.
    """
    # Request data from Boardgamegeek.com
    url = f"https://boardgamegeek.com/boardgame/{game_id}"
    response = requests.get(url)

    # Find and convert the data to a DataFrame
    if response.status_code == 200:
        df = collect_and_convert_data(response.content)

        # Organize the data into a dataframe and a list of attributes
        try:
            return process_data(df)
        except AttributeError:
            raise CollectBoardGameException(f"No board game data was found at {url}.")


def collect_and_convert_data(url_data: bytes) -> pd.DataFrame:
    """
    Takes raw url data and finds the board game data and converts it into a data frame.
    """
    # Pattern of the needed line of html
    pattern = r'GEEK\.geekitemPreload\s*=\s*({.*?});'

    soup = BeautifulSoup(url_data, 'html5lib')
    scripts = soup.find_all('script')
    for script in scripts:
        script_data = script.string
        if script_data:
            match_found = re.search(pattern, script_data, re.DOTALL)
            if match_found:
                data = match_found.group(1)
                data = json.loads(data)
                return pd.DataFrame(data)


def process_data(df: pd.DataFrame) -> tuple[list, list]:
    """
    Takes the url data as a data frame and returns a list of desired data and a list of attributes.
    """
    df = df.drop(['media', 'videogalleries'], axis=1).T

    # Check if item is an expansion
    is_expansion = df.iloc[0]['links']['expandsboardgame']
    if is_expansion:
        expands = int(is_expansion[0]['objectid'])
    else:
        expands = -1

    # Determine game rank or use -1 if item does not have a rank
    if df.iloc[0]['rankinfo'][0]['rank'] != '0':
        rank = int(df.iloc[0]['rankinfo'][0]['rank'])
    else:
        rank = -1

    # Check if a description exists
    if df.iloc[0]['short_description'] is None:
        description = 'None'
    else:
        description = df.iloc[0]['short_description']

    # Organize the needed data
    input_list = [
        int(df.iloc[0]['id']),
        df.iloc[0]['name'],
        expands,
        int(df.iloc[0]['yearpublished']),
        rank,
        float(df.iloc[0]['stats']['average']),
        float(df.iloc[0]['stats']['avgweight']),
        int(df.iloc[0]['minplayers']),
        int(df.iloc[0]['maxplayers']),
        int(df.iloc[0]['minplaytime']),
        int(df.iloc[0]['maxplaytime']),
        int(df.iloc[0]['minage']),
        description,
        df.iloc[0]['canonical_link']
    ]

    # Collect various category attributes as a list
    attributes = []
    categories = ['boardgamedesigner', 'boardgameartist', 'boardgamecategory', 'boardgamemechanic',
                  'boardgamefamily']
    for category in categories:
        attributes.append(get_data(category, df))

    return input_list, attributes


def get_data(category: str, df: pd.DataFrame) -> list:
    """
    Collects all entries for a specific board game category from a board game data frame. The result is returned
    as a list.
    """
    category_result = []
    for elem in df.iloc[0]['links'][category]:
        category_result.append(elem['name'])
    return category_result


if __name__ == '__main__':
    result = collect_data('97842')
    print(result)
    expansion_result = collect_data('132436')
    print(expansion_result)
