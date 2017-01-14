import requests
import csv
import os
import pandas as pd

def scrape(url):
    try:
        response_json = requests.get(url, headers={'user-agent': 'Mozilla/5.0', 'referer': 'http://stats.nba.com/scores/'}).json()
        headers = response_json['resultSets'][0]['headers']
        data = response_json["resultSets"][0]["rowSet"]
        return headers, data
    except:
        print "Encountered exception while scraping"

    return

def write_to_csv(data, headers, path):
	df = pd.DataFrame(data=data, columns=headers)
    df.to_csv(path)

def write_to_sql(data, headers, engine):
	df = pd.DataFrame(data=data, columns=headers)
	df.to_sql(engine)
