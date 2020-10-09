# import pandas as pd
# df = pd.DataFrame({'a b': [1,2,3], 'cd':[4,5,6]})

# for row in df.itertuples():
#     print(row[0])

# from settings import TABLE_KEYWORDS_MAP
# import pandas as pd

# table_columns = list(TABLE_KEYWORDS_MAP.keys())
# store_column_names = list(TABLE_KEYWORDS_MAP.values())




# print(table_columns)
# print(table_column_names)

# exit()

# print(map(table_keywords_map, table_columns))

# df = pd.DataFrame(None, columns=table_columns)
# print(df)


from bill import Bill
import pandas as pd

filename = '/home/totoy/Desktop/legis_output/bills_df/data_df_17.pickle'
print(filename)
df = pd.read_pickle(filename)
print(df)

for _, row in df.iterrows():
    print(row['bill_number'])
    break


a = Bill('17', row.to_dict())