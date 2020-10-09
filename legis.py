import os

from fuzzywuzzy import process

from fetch_reps import fetch_reps
from authors import Author

from congraph import Congraph

from bill import Bill

from settings import CIDS 
from settings import INPUT_PATH
from settings import BILLS_STORE_PATH

# TODO: REMOVE THESE - TEMPORARY STUFF
from settings import TABLE_KEYWORDS_MAP
table_keywords_map = TABLE_KEYWORDS_MAP

# TODO: Next steps - add party list members, create threshold - add unmapped names, JUST MAKE A PIPELINE FIRST! :)

input_path = INPUT_PATH
bills_store_path = BILLS_STORE_PATH
cids = CIDS


def legis(cid, congraph):
    '''TODO: Describe here
    123
    '''

    ###################
    ### Scrape Data ###
    ###################

    # load entity matcher 
    reps_df = fetch_reps(cid)

    # TODO: REMOVE THIS
    reps_df.rename(columns=table_keywords_map, inplace=True)

    import code 
    code.interact(local=locals())

    ###########################
    ### Create Author Nodes ###
    ###########################

    # get list of all reps under {cid} and update Author class
    author_names_master_list = reps_df['rep_name'].tolist()
    Author.update_masterlist_names(author_names_master_list)

    # convert df to data model and update KG
    authors_obj_list = []

    for rep in reps_df.itertuples():
        rep_obj = Author(name = rep.rep_name)
        rep_obj.set_term(
            cid=cid,
            province=rep.prov,
            district=rep.dist,
            party=rep.party,
            term=rep.term,
            bloc=rep.bloc,
            )

        # update author nodes
        congraph.update_author(rep_obj)

        # update locations nodes

        # update author-loc relationships


    # # loop through all the bills in {cid} congress
    # bills_path = input_path.format(cid=cid)
    # file_names = os.listdir(bills_path)

    # bill_list = []

    # for file_name in file_names:
    #     file_path = os.path.join(bills_path, file_name)

    #     bill = Bill(cid, file_path)
        
    #     for raw_author in bill.raw_authors:  
    #         mapped_author, score = process.extractOne(raw_author, authors_master_list)
    #         # logic here
    #         bill.add_mapped_author(mapped_author)
    #         bill_list.append(bill)
    



    # for bill_obj in bill_list:
    #     congraph.update_bill(bill_obj)
        # congraph.update_author(rep_obj)     
    # congress_list[cid].add_authore(reps)




    # update knowledge graph
    # for bill in bill_list:

        # TODO: add the updates based on bills 


if __name__ == "__main__":
    reset_graph = True
    congraph = Congraph("bolt://localhost:7687", "neo4j", "test")
    # congraph.reset() if reset_graph

    legis('17', congraph)
    
    congraph.close()
