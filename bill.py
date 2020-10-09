import re 
import pandas as pd

from settings import AUTHOR_KEYS
from settings import SHORT_TITLE_KEYS
from settings import BID_PATTERN
from settings import AUTHOR_TYPES_MAP

from authors import Author

author_keys = AUTHOR_KEYS
bid_pattern = BID_PATTERN
short_title_keys = SHORT_TITLE_KEYS
author_types = list(AUTHOR_TYPES_MAP.keys())

''' 
TODO_LIST = [
     'ra_number', 'adopted_number', 'concurrent_resolution', 
     'significance', 'nature', 'committee', 'date_urgent', 
     'second_reading', 'third_reading', 'senate_actions', 
     'conference_info','president_actions'
    ]
'''

class Bill:
    def __init__(self, cid, bill_dict):
        self.bill_dict = bill_dict
        self.cid = cid
        self.bid = bill_dict['bill_number']
        self.full_title = bill_dict['full_title']
        self.abstract = bill_dict['abstract']
        self.short_title = bill_dict['short_title']
        
        self.date_filed = None
        self._process_date_filed('date_filed')

        self.authors_list = list()
        self._process_authors_list(author_types)

        # TODO: process if needs further processing
        self.committee_actions = bill_dict['committee_actions']
        self.committee_rules = bill_dict['committee_rules']


    def _process_date_filed(self, date_filed_field):
        self.date_filed = pd.to_datetime(self.bill_dict[date_filed_field])


    def _process_authors(self, authors_list_raw, author_type):
        authors = list()
        for author_name_raw in authors_list_raw:
            author = Author(author_name_raw)
            author.set_author_type(author_type)
            authors.append(author)
        return authors


    def _process_authors_list(self, author_types):
        for author_type in author_types:
            authors = self._process_authors(self.bill_dict[author_type], author_type)
            self.authors_list.extend(authors)

    


# class Bill_Data_Model:
#     def __init__(self, congress, file_path):
#         self.file_path = file_path
#         self.congress = congress
#         self.raw_authors = None
#         self.mapped_authors = []
#         self.unmapped_authors = []
#         with open(file_path, 'r') as bill:
#             self.bill_texts = bill.read().split('\n')

#         self._extract_bill_id()
#         self._extract_description()
#         self._extract_short_title()
#         self._extract_authors()
#         # self._process_authors()
    
    
#     def _extract_bill_id(self):
#         for bill_text in self.bill_texts:
#             bid = re.findall(bid_pattern, bill_text)[0]
#             if bid:
#                 self.bid = bid
#                 return
            
#         # TODO: trigger push to bin
#         return None 

    
#     def _extract_description(self):
#         # TODO: this might be faulty, check this in the future
#         self.description = self.bill_texts[1]
#         return 

    
#     def _extract_short_title(self):
#         for bill_text in self.bill_texts:
#             try: 
#                 key, value = bill_text.split(':')
#             except:
#                 continue
            
#             if key in short_title_keys:
#                 self.short_title = value.strip()
#                 return
            
#         # TODO: trigger push to bin
#         return None 
    
    
#     def _extract_authors(self):
#         for bill_text in self.bill_texts:
#             try:
#                 key, authors = bill_text.split(':')
#             except:
#                 continue
            
#             if key in author_keys:
#                 authors = authors.split(';')
#                 self.raw_authors = [author.strip() for author in authors if author]
#                 # self.raw_authors = list(map(str.strip, authors))
#                 return
            
#         # TODO: trigger push to bin
#         return None 


#     def add_mapped_author(self, mapped_author):
#         self.mapped_authors.append(mapped_author)
#         # self.unmapped_authods = unmapped_authors




    # # CHANGE PROCESS AUTHORS
    # def _process_authors(self):
    #     authors = []
    #     for author in self.raw_authors:
    #         authors.append(Author(author, self.congress))
        
    #     self.authors = authors