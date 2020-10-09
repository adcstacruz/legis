import os 

# base paths TODO: make environment paths
OUTPUT_PATH = '/home/totoy/Desktop/legis_output'
INPUT_PATH = '/home/totoy/Downloads/Legis/legis/dump/{cid}'

# scraper parameters
REPS_STORE_PATH = os.path.join(OUTPUT_PATH, 'congress_reps')
REPS_FILENAME = 'reps_{cid}.pickle'

# bills paramteres
DF_STORE_NAME = 'data_df_{cid}.pickle'
BILLS_STORE_PATH = os.path.join(OUTPUT_PATH, 'bills_df')
BILLS_FIELD_NAMES = [
    'bill_number', 'ra_number', 'adopted_number', 
    'concurrent_resolution', 'full_title', 'abstract', 
    'short_title', 'date_filed', 'significance', 
    'nature', 'committee', 'date_urgent', 
    'principal', 'co_authors_journal', 'co_authors_committee',
    'co_authors_final', 'authors_withdraw', 'committee_actions',
    'committee_rules', 'second_reading', 'third_reading', 
    'senate_actions', 'conference_info','president_actions'
    ]


URLS = {'17': "https://en.wikipedia.org/wiki/17th_Congress_of_the_Philippines"}
CIDS = list(URLS.keys())

# TABLE KEY WORDS
REP_TABLE_KEYWORDS_MAP = {
    "Province/City": "prov", 
    "District": "dist",
    "Representative.1": "rep_name",
    "Party": "party",
    "Term": "term",
    "Bloc": "bloc",
} 

# TODO: ADD SENATE
# NOTES: Needs column name cleaning
# TODO: ADD PARTLIST

# bills settings 
BID_KEY_PATTERN = ''
BID_PATTERN = '^H[a-zA-Z]*\d+\d$'
AUTHOR_KEYS = ['Principal Author/s']
SHORT_TITLE_KEYS = ['Short Title']





############ TODO LIST ###########

'''
# TODO: 


PEOPLE:
* ADD - 1) sex; 2) region; 3) island group; 4) reading
* READING -  

* Social welfare categories?

* BILL - BILL OR RESOLUTION:
* Significance - 
* Nature - social welfare, infrostructure 


Network - X


Bi-modal: 

# EDGES -> 



(people)

(term)

(bill)

'''