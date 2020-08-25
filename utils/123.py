
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

from settings import URLS
from settings import REPS_STORE_PATH, REPS_FILENAME
from settings import TABLE_KEYWORDS


urls = URLS
reps_store_path = REPS_STORE_PATH
reps_filename = REPS_FILENAME
table_columns = TABLE_KEYWORDS


def fetch_reps(cid):
    reps_filepath = os.path.join(reps_store_path, reps_filename.format(cid=cid))
    
    if os.exists(reps_filepath):
        return pd.read_pickle(reps_filepath)    

    reps_df = scrape_reps(url)
    reps_df.to_pickle(reps_filepath)
    return reps_df



def scrape_reps(url):
    html_content = requests.get(url).content
    soup = BeautifulSoup(html_content, 'lxml')
    candidate_tables = soup.find_all("table", {"class": "wikitable sortable"})

    table = None
    best_score = 0
    for c_table in candidate_tables:
        c_table_ths = c_table.find_all('th')

        temp_score = 0
        for th in c_table_ths:
            if th.text.replace('\n', ' ').lower().strip() in table_columns:
                temp_score +=1

        if best_score < temp_score:
            table = c_table
            best_score = temp_score

    table_rows = table.find_all('tr')

    results = []
    temp_province = None
    for tr in table_rows[1:]:
        row_elements = tr.find_all('td')

        row = [re.sub(r"\[.*?\]", "", row_elem.text.strip()) for row_elem in row_elements if row_elem.text.strip()]

        if len(row) == len(table_columns)-1:
            row.insert(0, temp_province)
        else:
            temp_province = row[0]

        if row:
            results.append(row)
            
    return pd.DataFrame(results, columns=table_columns)


