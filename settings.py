'''Pipeline Settings.'''

import os 

# base paths TODO: make environment paths
OUTPUT_PATH = '/home/totoy/Desktop/legis_output'
INPUT_PATH = '/home/totoy/Downloads/Legis/legis/dump/{cid}'

# scraper parameters
REPS_STORE_PATH = os.path.join(OUTPUT_PATH, 'congress_reps')
REPS_FILENAME = 'reps_{cid}.pickle'

# bills paramteres
DF_STORE_NAME = 'bills_df_{cid}.pickle'
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
    'Province/City': 'prov', 
    'District': 'dist',
    'Representative.1': 'rep_name',
    'Party': 'party',
    'Term': 'term',
    'Bloc': 'bloc',
} 

AUTHOR_TYPES_MAP = {
    'principal': 'IS_AUTH_P',
    'co_authors_journal': 'IS_CO_AUTH_J',
    'co_authors_committee': 'IS_CO_AUTH_C', 
    'co_authors_final': 'IS_CO_AUTH_F', 
    'authors_withdraw': 'IS_CO_WD',
    }


# TODO: ADD SENATE
# NOTES: Needs column name cleaning
# TODO: ADD PARTLIST

# bills settings 
BID_KEY_PATTERN = ''
BID_PATTERN = '^H[a-zA-Z]*\d+\d$'
AUTHOR_KEYS = ['Principal Author/s']
SHORT_TITLE_KEYS = ['Short Title']
