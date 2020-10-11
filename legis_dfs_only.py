import os

from fuzzywuzzy import process

from fetch_authors import fetch_reps
from fetch_bills import fetch_bills

from authors import Author
from bill import Bill
from congraph import Congraph

from settings import CIDS 
from settings import INPUT_PATH
from settings import BILLS_STORE_PATH

# TODO: Next steps - add party list members, create threshold - add unmapped names, JUST MAKE A PIPELINE FIRST! :)

input_path = INPUT_PATH
bills_store_path = BILLS_STORE_PATH
cids = CIDS


def legis(cid, congraph):
    '''TODO: DESC HERE
    '''

    ########################################
    ### Scrape and Load Data (wiki data) ###
    ########################################
    reps_df = fetch_reps(cid)

    ################################################
    ### Parse Bill Texts and Convert store as DF ###
    ################################################

    bills_df = fetch_bills('17')
    


if __name__ == "__main__":
    congraph = None
    legis('17', congraph)
