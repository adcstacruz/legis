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


    ########################################
    ### Create Author and Location Nodes ###
    ########################################

    # TODO: Get initial list based from the KG Author nodes
    author_names_master_list = []

    ### REPS ###

    # get list of all reps under {cid} and update Author class
    author_names_master_list.extend(reps_df['rep_name'].tolist())
    Author.update_masterlist_names(author_names_master_list, extend=False)

    # convert df to data model and update KG
    reps_obj_list = []
    for rep in reps_df.itertuples():
        rep_obj = Author(name = rep.rep_name)
        rep_obj.set_mapped(True)
        rep_obj.set_term(
            cid=cid,
            province=rep.prov,
            district=rep.dist,
            party=rep.party,
            term=rep.term,
            bloc=rep.bloc,
            )

        # TODO: rep_obj.set_author_mem('rep')

        reps_obj_list.append(rep_obj)

        # update author nodes
        congraph.update_auth_nodes(rep_obj)

        # update locations nodes
        congraph.update_loc_nodes(rep_obj)

        # update author-loc relationships
        congraph.update_loc_auth_rels(rep_obj)
    
    del reps_df

    ### SEN ###
    # TODO:

    ### PARTY ###
    # TODO:

    ################################################
    ### Parse Bill Texts and Convert store as DF ###
    ################################################

    bills_df = fetch_bills('17')
    

    #########################
    ### Create Bill Nodes ###
    #########################

    for _, row in bills_df.iterrows():
        bill_obj = Bill(cid, row.to_dict())

        # update bill nodes
        congraph.update_bill_nodes(bill_obj)

        # update bill-author nodes
        congraph.update_bill_auth_rels(bill_obj)
        

    del bills_df

    print('GRAPHINIFICATION DONE! YEY!')


if __name__ == "__main__":
    clear_graph = True
    congraph = Congraph("bolt://localhost:7687", "neo4j", "test")
    
    if clear_graph:
        congraph.clear_graph() 

    legis('17', congraph)
    
    congraph.close()