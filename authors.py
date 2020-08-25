from settings import CIDS

cids = CIDS


class Author:
    def __init__(self, name):
        self.name = name
        self.terms = {}

    def set_name(self, matched_name, confidence):
        self.name = matched_name


    def set_potential_names(self, matched_names, confidence):
        pass

    def add_term(self, term):
        self.terms[term.cid] = term
        

class Term:
    def __init__(self, cid, province, district, party, term, bloc):
        self.cid = cid
        self.province = province
        self.district = district
        self.party = party 
        self.term = term
        self.bloc = bloc
        self.bills = [] #TODO: might be just a tuple ('P', 'HBXXXX')

    def add_bill():
        pass
        