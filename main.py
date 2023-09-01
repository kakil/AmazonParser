from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

import requests
import csv
import os
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent
READY = BASE_DIR / 'ready'

API_KEY = '1fb6e6ec-b0d4-4c30-b819-7c6cb86cf795'  # add scrapeops.io api key here
# API_KEY = os.getenv("SCRAPEOPS_API_KEY")

titles = []

keys = ['adult coloring book for women naughty', ]  # add the keyphrases for parsing here.


def write_csv(data):

    name = ','.join(keys)

    if len(name) > 100:
        name = name[:100]

    with open(f'{READY}/{name}.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)


def get_html(url):
    response = requests.get(
      url='https://proxy.scrapeops.io/v1/',
      params={
          'api_key': API_KEY,
          'url': url,

      },
    )
    response.encoding = 'utf-8'

    return response.text


def main():
    for elem in keys:
        url = 'https://www.amazon.com/s?k=' + elem.replace(' ', '+')

        # print(f'Parsing titles for the key phrase "{elem}"\n'f'Link: {url}')

        html = get_html(url)
        
        # print("HTML Content: ", html[:200])  # Print the first 200 characters of HTML

        soup = BeautifulSoup(html, 'lxml')

        block = soup.select('div[cel_widget_id*="MAIN-SEARCH_RESULTS"]')

        # print("Number of blocks found: ", len(block))  # Print the number of blocks found

        for i in block:
            title = i.find('h2')
            if title:
                title = title.text
                data = {'title': title}

                if title not in titles:
                    titles.append(title)
                    write_csv(data)

        print(f'{len(block)} titles are written in the CSV file (ready folder)')



if __name__ == '__main__':
    if not API_KEY:
        print('Register a free account on scrapeops.io, copy the API key,\n'
              'and assign it to the string constant API_KEY in the main.py file')
    else:
        main()
