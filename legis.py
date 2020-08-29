import os

from fuzzywuzzy import process


from fetch_reps import fetch_reps
from authors import Author
from authors import Term

from congraph import Congraph

from bill import Bill

from settings import CIDS 
from settings import INPUT_PATH

# TODO: Next steps - add party list members, create threshold - add unmapped names, JUST MAKE A PIPELINE FIRST! :)


input_path = INPUT_PATH
cids = CIDS

congress_list = {}
authors_list = {}
bill_list = {}

authors_master_list = []


# TODO: REMOVE THIS - TEMPORARY STUFF
from settings import TABLE_KEYWORDS_MAP
table_keywords_map = TABLE_KEYWORDS_MAP


# TODO: create a class for this - there might be better way of entity matching
def entity_linker():
    pass 



def legis(cid, congraph):
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
        authors_master_list.append(rep_obj.name)


        congraph.update_author(rep_obj)



    # loop through all the bills in {cid} congress
    bills_path = input_path.format(cid=cid)
    file_names = os.listdir(bills_path)


    bill_list = []

    for file_name in file_names:
        file_path = os.path.join(bills_path, file_name)

        bill = Bill(cid, file_path)
        
        for raw_author in bill.raw_authors: 
         
            
            mapped_author, score = process.extractOne(raw_author, authors_master_list)
            # logic here
            bill.add_mapped_author(mapped_author)

            bill_list.append(bill)
    



    for bill_obj in bill_list:
        congraph.update_bill(bill_obj)
        # congraph.update_author(rep_obj)     
    # congress_list[cid].add_authore(reps)




    # update knowledge graph
    # for bill in bill_list:

        # TODO: add the updates based on bills 











# load entity matcher

# for bill in bills

if __name__ == "__main__":
    congraph = Congraph("bolt://localhost:7687", "neo4j", "test")
    legis('17', congraph)
    # greeter.print_greeting("hello, world")
    # greeter.print_greeting("TRIAL")
    congraph.close()

    # import code 
    # code.interact(local=locals())