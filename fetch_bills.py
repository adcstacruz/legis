'''Congress Bill Fetcher.'''

import os
import time

import re
import pandas as pd

from settings import DF_STORE_NAME, BILLS_STORE_PATH, INPUT_PATH


def fetch_bills(cid):
    # i/o directories
    bills_df_name = DF_STORE_NAME.format(cid=cid)
    bills_df_store_path = BILLS_STORE_PATH
    bills_df_path = os.path.join(
        bills_df_store_path, 
        bills_df_name
        )

    if not os.path.exists(bills_df_path):
        raw_bills_dir_path = INPUT_PATH.format(cid=cid)
        bill_text_to_df(
            raw_bills_dir_path,
            bills_df_path
        )
    
    return pd.read_pickle(bills_df_path)


def bill_text_to_df(raw_bills_dir_path, bills_df_path):
    # load
    list_files = os.listdir(raw_bills_dir_path)

    ##### create an empty dataframe
    fields = ['bill_number',#
    'ra_number',#
    'adopted_number', #
    'concurrent_resolution', #
    'full_title',#
    'abstract', #
    'short_title', #
    'date_filed',#
    'significance', #
    'nature', #
    'committee', #
    'date_urgent', #
    'principal',#
    'co_authors_journal',
    'co_authors_committee',
    'co_authors_final',
    'authors_withdraw',
    'committee_actions',
    'committee_rules',
    'second_reading',
    'third_reading',
    'senate_actions',
    'conference_info',
    'president_actions']

    df = pd.DataFrame(columns = fields) 

    counter = 0
    ##### parse each file
    for textfile in list_files:
        counter += 1
        with open(os.path.join(raw_bills_dir_path, textfile)) as file:
            table_cells = [line.rstrip() for line in file]
        
        i=-1
        bill_number = ""
        ra_number = ""
        adopted_number = ""
        concurrent_resolution = ""
        full_title = ""
        abstract = ""
        short_title = ""
        date_filed = ""
        significance = ""
        nature = ""
        committee = ""
        date_urgent = ""

        principal = []
        co_author = ""
        co_authors_journal = []
        co_authors_committee = []
        co_authors_final = []
        authors_withdraw = []
        
        committee_actions = []
        committee_rules = []
        second_reading = []
        third_reading = []
        senate_actions = []
        conference_info = []
        president_actions = []

        for cells in table_cells:
            i += 1
            if re.search(re.compile(r'House Bill/Resolution NO. '), cells) != None:
                bill_number = re.findall('House Bill/Resolution NO. (.*\'?)', cells)[0].strip()
                continue
            if cells[:17] == 'REPUBLIC ACT NO. ':
                ra_number = re.findall('REPUBLIC ACT NO. ', cells)[0].strip()
                continue
            if re.search(re.compile(r'ADOPTED AS RESOLUTION NO. '), cells) != None:
                adopted_number = re.findall('ADOPTED AS RESOLUTION NO. (.*\'?)', cells)[0].strip()
                continue
            if re.search(re.compile(r'COUNTERPART HOUSE BILL/CONCURRENT RESOLUTION: '), cells) != None:
                concurrent_resolution = re.findall('COUNTERPART HOUSE BILL/CONCURRENT RESOLUTION: (.*\'?)', cells)[0].strip()
                continue
            if re.search(re.compile(r'FULL TITLE : '), cells) != None:
                full_title = re.findall('FULL TITLE : (.*\'?)', cells)[0].strip()
                continue
            if re.search(re.compile(r'ABSTRACT : '), cells) != None:
                abstract = re.findall('ABSTRACT : (.*\'?)', cells)[0].strip()
                continue
            if re.search(re.compile(r'SHORT TITLE : '), cells) != None:
                short_title = re.findall('SHORT TITLE : (.*\'?)', cells)[0].strip()
                continue
            if re.search(re.compile(r'ALIAS NAME : '), cells) != None:
                short_title = re.findall('ALIAS NAME : (.*\'?)', cells)[0].strip()
                continue
            if re.search(re.compile(r'PRINCIPAL AUTHOR/S : '), cells) != None:
                principal = re.findall('PRINCIPAL AUTHOR/S : (.*\'?)', cells)[0]
                principal = re.sub(", M.D.,", ' M.D.,', principal)
                principal = principal.split(",")
                principal = [(x+","+y).strip() for x,y in zip(principal[0::2], principal[1::2])]
                continue
            if re.search(re.compile(r'DATE FILED : '), cells) != None:
                date_filed = re.findall('DATE FILED : (.*\'?)', cells)[0].strip()
                continue
            if re.search(re.compile(r'SIGNIFICANCE: '), cells) != None:
                significance = re.findall('SIGNIFICANCE: (.*\'?)', cells)[0].strip()
                continue
            if re.search(re.compile(r'NATURE : '), cells) != None:
                nature = re.findall('NATURE : (.*\'?)', cells)[0].strip()
                continue
            if cells == "CO-AUTHORS (Journal Entries) :":
                for remaining in table_cells[i+1:]:
                    if re.search(re.compile(r'^[0-9]+\. '), remaining) != None:
                        co_author = re.findall('[0-9]+\.(.*\'?)\(.*\)$', remaining)[0].strip()
                        co_authors_journal.append(co_author)
                    else:
                        break
                continue
            if cells == "AUTHORS(Committee Report) :":
                for remaining in table_cells[i+1:]:
                    if re.search(re.compile(r'^[0-9]+\. '), remaining) != None:
                        co_author = re.findall('[0-9]+\.(.*\'?)', remaining)[0].strip()
                        co_authors_committee.append(co_author)
                    else:
                        break
            if cells == "AUTHORS(Final/Third Reading) :":
                for remaining in table_cells[i+1:]:
                    if re.search(re.compile(r'^[0-9]+\. '), remaining) != None:
                        co_author = re.findall('[0-9]+\.(.*\'?)', remaining)[0].strip()
                        co_authors_final.append(co_author)
                    else:
                        break
            if cells == "AUTHORSHIP WITHDRAWALS:":
                for remaining in table_cells[i+1:]:
                    if remaining == "()" or remaining == 'ACTIONS TAKEN BY THE COMMITTEE' or remaining == 'ACTIONS TAKEN BY THE COMMITTEE ON RULES' or remaining[:45] == 'COUNTERPART HOUSE BILL/CONCURRENT RESOLUTION:' or remaining[:25] == 'DATE CERTIFIED AS URGENT:': break
                    co_author = re.findall('(.*\'?)\(.*\)$', remaining)[0].strip()
                    authors_withdraw.append(co_author)
            if re.search(re.compile(r'DATE CERTIFIED AS URGENT:'), cells) != None:
                date_urgent = re.findall('DATE CERTIFIED AS URGENT:(.*\'?)', cells)[0].strip()
                continue
            if cells == "ACTIONS TAKEN BY THE COMMITTEE":
                for remaining in table_cells[i+1:]:
                    if remaining == "ACTIONS TAKEN BY THE COMMITTEE ON RULES": break
                    committee_actions.append(remaining)
            if cells == "ACTIONS TAKEN BY THE COMMITTEE ON RULES":
                for remaining in table_cells[i+1:]:
                    if remaining[:29] == "REFERRAL TO THE COMMITTEE ON ":
                        committee = remaining[29:][:-14]
                    if remaining == "SECOND READING INFORMATION": break
                    committee_rules.append(remaining)
            if cells == "SECOND READING INFORMATION":
                for remaining in table_cells[i+1:]:
                    if remaining == "THIRD READING INFORMATION": break
                    second_reading.append(remaining)
            if cells == "THIRD READING INFORMATION":
                for remaining in table_cells[i+1:]:
                    if remaining == "ACTIONS TAKEN BY THE SENATE/HOUSE": break
                    third_reading.append(remaining)
            if cells == "ACTIONS TAKEN BY THE SENATE/HOUSE":
                for remaining in table_cells[i+1:]:
                    if remaining == "CONFERENCE COMMITTEE INFORMATION": break
                    senate_actions.append(remaining)
            if cells == "CONFERENCE COMMITTEE INFORMATION":
                for remaining in table_cells[i+1:]:
                    if remaining == "ACTIONS TAKEN BY THE PRESIDENT": break
                    conference_info.append(remaining)
            if cells == "ACTIONS TAKEN BY THE PRESIDENT":
                for remaining in table_cells[i+1:]:
                    president_actions.append(remaining)
            
        data = [[bill_number,
                ra_number,
                adopted_number,
                concurrent_resolution,
                full_title,
                abstract,
                short_title,
                date_filed,
                significance,
                nature,
                committee,
                date_urgent,
                principal,
                co_authors_journal,
                co_authors_committee,
                co_authors_final,
                authors_withdraw,
                committee_actions,
                committee_rules,
                second_reading,
                third_reading,
                senate_actions,
                conference_info,
                president_actions]]
        
        data = pd.DataFrame(data, columns = fields)
        
        df = pd.concat([df, data])
        
        print(counter, "out of", len(list_files))


    # clean dataframe
    df.reset_index(inplace=True)
    df['date_filed'] = pd.to_datetime(df['date_filed'])

    # store dataframe
    df.to_pickle(bills_df_path)