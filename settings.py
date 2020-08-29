import os 


# base paths TODO: make environment paths
OUTPUT_PATH = '/home/totoy/Desktop/legis_output'
INPUT_PATH = '/home/totoy/Downloads/Legis/legis/dump/{cid}W'

# scraper params
REPS_STORE_PATH = os.path.join(OUTPUT_PATH, 'congress_reps')
REPS_FILENAME = 'reps_{cid}.pickle'


URLS = {'17': "https://en.wikipedia.org/wiki/17th_Congress_of_the_Philippines"}
CIDS = list(URLS.keys())

TABLE_KEYWORDS = ["province/city", "district", 
                  "representative", "party", 
                  "term", "bloc"]


TABLE_KEYWORDS_MAP = {
    "province/city": "prov", 
    "district": "dist",
    "representative": "rep",
    "part": "party",
    "term": "term",
    "bloc": "bloc",
} 



# bills settings 
AUTHOR_KEYS = ['Principal Author/s']
SHORT_TITLE_KEYS = ['Short Title']
BID_PATTERN = '^H[a-zA-Z]*\d+\d$'


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