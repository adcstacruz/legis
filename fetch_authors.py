'''Congress Enitity Fetcher.'''

import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

from settings import URLS
from settings import REPS_STORE_PATH, REPS_FILENAME
from settings import REP_TABLE_KEYWORDS_MAP

urls = URLS
reps_store_path = REPS_STORE_PATH
reps_filename = REPS_FILENAME

rep_table_map = REP_TABLE_KEYWORDS_MAP
rep_table_kw = list(rep_table_map.keys())


def clean_data(x): # TODO: move to utils
    # remove reference texts
    x = re.sub(r"\[.*?\]", "", x.strip())
    # TODO: removal of indices (haven't checked other use cases)
    return x           


def get_common_fields_len(fields_1, fields_2): 
    set_1 = set(fields_1) 
    set_2 = set(fields_2) 
    return len(list(set_1 & set_2))
        

def fetch_reps(cid): # TODO: move to utils
    '''Representatives Fetcher.
        
        input: string representation of congress id
        output: dataframe of representatives
        others: stores the data if not present in the data directory
    
    '''

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
    return reps_df


def scrape_reps(url):
    '''Representative Data Scraper.

        input: string url
        output: dataframe of representatives
    
    '''

    # find the reps table
    candidate_tables = pd.read_html(url)

    # find table in html
    table = None
    best_match_len = 0

    for c_table in candidate_tables:
        cf_len = get_common_fields_len(
            c_table.columns.tolist(),
            rep_table_kw
        )
        print(cf_len)
        if best_match_len < cf_len:
            table = c_table
            best_match_len = cf_len

    # rename and filter fields
    table.rename(columns=rep_table_map, inplace=True)
    table = table[list(rep_table_map.values())]

    # remove reference texts 
    table['rep_name'].apply(clean_data)
    
    return table


def scrape_senators():
    pass


def scrape_partylist_mem():
    pass


if __name__ == "__main__":
    reps_df = fetch_reps('17')

    # for QA
    import code
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    code.interact(local=locals())
