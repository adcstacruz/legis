import os

from fetch_reps import fetch_reps
from authors import Author
from authors import Term

from settings import CIDS 
from settings import INPUT_PATH




input_path = INPUT_PATH
cids = CIDS

congress_list = {}
authors_list = {}

authors = []


# TODO: REMOVE THIS - TEMPORARY STUFF
from settings import TABLE_KEYWORDS_MAP
table_keywords_map = TABLE_KEYWORDS_MAP



def legis(cid):
    # instantiate congress
    # congress_list[cid] = Congress(cid)

    # instantiate authors list


    # load entity matcher 
    reps_df = fetch_reps(cid)

    # TODO: REMOVE THIS
    reps_df.rename(columns=table_keywords_map, inplace=True)


    # create the list of authors in congress
    for rep in reps_df.itertuples():
        rep_obj = Author(name = rep.rep)
        rep_obj.add_term(
            Term(cid=cid,
                province=rep.prov,
                district=rep.dist,
                party=rep.party,
                term=rep.term,
                bloc=rep.bloc
                )
            )
        
        authors_list[rep_obj.name] = rep_obj

    # loop through all the bills in {cid} congress
    bills_path = input_path.format(cid=cid)
    file_names = os.listdir(bills_path)

    for file_name in file_names:
        file_path = os.path.join(bills_path, file_name)
        print(file_path)    

    return None
    
    # congress_list[cid].add_authore(reps)



    # update knowledge graph










# load entity matcher

# for bill in bills

if __name__ == "__main__":
    authors_list = legis('17')


    import code 
    code.interact(local=locals())