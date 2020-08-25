import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

from settings import URLS


from settings import REPS_STORE_PATH, REPS_FILENAME
from settings import TABLE_KEYWORDS_MAP


urls = URLS
reps_store_path = REPS_STORE_PATH
reps_filename = REPS_FILENAME

table_keywords_map = TABLE_KEYWORDS_MAP
table_columns = list(table_keywords_map.keys())



def fetch_reps(cid):
    reps_filepath = os.path.join(reps_store_path, reps_filename.format(cid=cid))
    
    if os.path.exists(reps_filepath):
        print("Rep list available")
        return pd.read_pickle(reps_filepath)    

    print("Rep list NOT available. Scraping...")
    # scrape the representatives
    reps_df = scrape_reps(urls[cid])
    print("Done")

    #storing the representatives df
    if not os.path.exists(reps_store_path):
        os.makedirs(reps_store_path)

    reps_df.to_pickle(reps_filepath)
    reps_df.rename(columns=table_keywords_map, inplace=True)  

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


