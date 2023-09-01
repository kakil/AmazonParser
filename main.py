from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from pathlib import Path
import requests
import csv
import os
from bs4 import BeautifulSoup

# FastAPI app
app = FastAPI()

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).parent
READY = BASE_DIR / 'ready'

titles = []


def write_csv(data, keys):
    name = ','.join(keys)

    if len(name) > 100:
        name = name[:100]

    with open(f'{READY}/{name}.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)


def get_html(url, api_key):
    response = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params={
            'api_key': api_key,
            'url': url,
        },
    )
    response.encoding = 'utf-8'

    return response.text


@app.get("/scrape/")
async def scrape(key: str, api_key: str):
    if not api_key:
        return JSONResponse(content={
            'error': 'Please provide a valid API key'
        }, status_code=400)

    keys = [key]
    for elem in keys:
        url = 'https://www.amazon.com/s?k=' + elem.replace(' ', '+')
        html = get_html(url, api_key)
        soup = BeautifulSoup(html, 'lxml')

        block = soup.select('div[cel_widget_id*="MAIN-SEARCH_RESULTS"]')

        for i in block:
            title = i.find('h2')
            if title:
                title = title.text
                data = {'title': title}

                if title not in titles:
                    titles.append(title)
                    write_csv(data, keys)

    return JSONResponse(content={
        'message': f'{len(block)} titles are written in the CSV file (ready folder)',
        'titles': titles
    })
