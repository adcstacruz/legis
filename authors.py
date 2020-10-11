'''Author Data Model.'''

from settings import CIDS

from settings import AUTHOR_TYPES_MAP

author_types_map = AUTHOR_TYPES_MAP

cids = CIDS

class Author:

    masterlist_names = []

    def __init__(self, name):
        self.name = name
        self.name_raw = name
        self.name_matched = None
        self.is_matched = False


    def set_term(self, cid, province, district, party, term, bloc):
        self.cid = cid
        self.province = province
        self.district = district
        self.party = party 
        self.term = term
        self.bloc = bloc


    def process_name_match():
        # TODO: add entitiy linking
       
        if confidence > match_th:
            self.name_matched = (name_matched, confidence)
            self.name = name_matched
            self.is_matched = True


    def set_mapped(self, map_logic):
        self.is_matched = map_logic


    def set_author_type(self, author_type):
        self.author_type = author_types_map[author_type]


    @classmethod
    def update_masterlist_names(cls, new_master_list, extend=True):
        if extend:
            cls.masterlist_names.extend(new_master_list)
        else:
            cls.masterlist_names = new_master_list
