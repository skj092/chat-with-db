import pandas as pd
from pathlib import Path
import sqlite3


data_path = Path("/home/sonujha/rnd/text2sql/dbsetup/")
df = pd.read_csv(data_path/'user_features.csv')

# add df in the db
con = sqlite3.connect(data_path/'user_features.db')
cur = con.cursor()

df.to_sql('user_features', con, if_exists='replace', index=False)
con.commit()
con.close()

# test the db
con = sqlite3.connect(data_path/'user_features.db')
cur = con.cursor()

query = "SELECT * FROM user_features LIMIT 5"
result = pd.read_sql_query(query, con)

print(result)
con.close()
