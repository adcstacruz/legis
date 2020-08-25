# import pandas as pd
# df = pd.DataFrame({'a b': [1,2,3], 'cd':[4,5,6]})

# for row in df.itertuples():
#     print(row[0])


from settings import TABLE_KEYWORDS_MAP
import pandas as pd

table_columns = list(TABLE_KEYWORDS_MAP.keys())
table_column_names = list(TABLE_KEYWORDS_MAP.values())




print(table_columns)
print(table_column_names)

exit()

print(map(table_keywords_map, table_columns))

df = pd.DataFrame(None, columns=table_columns)
print(df)