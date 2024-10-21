from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import sqlite3
from pathlib import Path

data_path = Path("/home/sonujha/rnd/text2sql/dbsetup/")
db = sqlite3.connect(data_path/'user_features.db')


# Use proper SQLite URI format
db_uri = f"sqlite:///{data_path/'user_features.db'}"
db = SQLDatabase.from_uri(db_uri)


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(
    llm, db=db, agent_type="openai-tools", verbose=True)
agent_executor.invoke(
    "list the total number of users"
)
