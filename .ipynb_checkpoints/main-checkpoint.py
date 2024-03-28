import json
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://boardgamegeek.com/boardgame/97842/last-will"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html5lib')
    scripts = soup.find_all('script')

    pattern = r'GEEK\.geekitemPreload\s*=\s*({.*?});'
    for script in scripts:
        script_data = script.string
        if script_data:
            match_found = re.search(pattern, script_data, re.DOTALL)
            if match_found:
                data = match_found.group(1)
                data = json.loads(data)
                df = pd.DataFrame(data.get('item'))
                print(df.head())
                break
