from settings import CIDS

cids = CIDS

class Author:

    masterlist_names = []

    def __init__(self, name):
        self.name = name
        self.name_raw = name
        self.terms = {}
        self.is_matched = False


    def set_term(self, cid, province, district, party, term, bloc):
        self.cid = cid
        self.province = province
        self.district = district
        self.party = party 
        self.term = term
        self.bloc = bloc


    def process_name_match():        
        if confidence > match_th:
            self.matched_name = (matched_name, confidence)
            self.name = matched_name
            self.is_matched = True


    def set_author_type(self, author_type):
        self.author_type = author_type


    @classmethod
    def update_masterlist_names(cls, new_master_list):
        cls.masterlist_names = new_master_list
