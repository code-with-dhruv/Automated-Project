#!/usr/bin/env python
'''
Developed with Love
4th dec 2022 
'''
from __future__ import print_function
import time
import pandas as pd
import woslite_client
from woslite_client.rest import ApiException
from pprint import pprint
import numpy  
configuration = woslite_client.Configuration()
configuration.api_key['X-ApiKey'] = 'e9bc939b6ec9edb8c7cb88f03da101f88bdb4942'

# create an instance of the API class
integration_api_instance = woslite_client.IntegrationApi(
  woslite_client.ApiClient(configuration))
search_api_instance = woslite_client.SearchApi(
  woslite_client.ApiClient(configuration))

database_id = 'WOS'
b=input("Enter the Query:\n")

usr_query = 'AU=("{}")'.format(b)
count = 100  
first_record = 1
lang = 'en'
sort_field = 'PY+D'

api_response = search_api_instance.root_get(database_id,
                                            usr_query,
                                            count,
                                            first_record,
                                            lang=lang,
                                            sort_field=sort_field)

output = []

for i in range(1, count):
  try:
    title = str(api_response.data[i].title.title[0]).replace(","," ")
  
    for j in range(1, len(api_response.data[i].author.authors)):
      author = str(api_response.data[i].author.authors[j]).replace(","," ")
    ut = str(api_response.data[i].ut).replace(","," ")
  except:
    pass
  

  line = {'Title': title, 'authors': author, 'id': ut}
  output.append(line)
df = pd.DataFrame(output)
df.to_csv('output2.csv')
print("DONE")

import sqlite3


conn = sqlite3.connect("sql.db")
cur = conn.cursor()
sql = "DROP TABLE home_excel"

cur.execute(sql)
sql = """
CREATE TABLE home_excel (
  id TEXT,
  Title TEXT,
  authors TEXT,
  dbid TEXT
  )"""
cur.execute(sql)
print("Database has been created")
conn.commit()
conn.close()

conn = sqlite3.connect("sql.db")
cur = conn.cursor()
with open('output2.csv','r') as file:
  count=0
  for row in file:
    print(row)
    cur.execute("INSERT INTO home_excel VALUES (?,?,?,?)",row.split(","))
    conn.commit()
    count+=1
  conn.close()
  print(count)

"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hello.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
