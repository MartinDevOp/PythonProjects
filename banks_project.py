"""You have been hired as a data engineer by research organization. Your boss has asked you to create a code that can be used to
 compile the list of the top 10 largest banks in the world ranked by market capitalization in billion USD. Further, 
 the data needs to be transformed and stored in GBP, EUR and INR as well, in accordance with the exchange rate information 
 that has been made available to you as a CSV file. The processed information table is to be saved locally in a CSV format 
 and as a database table.
Your job is to create an automated system to generate this information so that the same can be executed in every financial
quarter to prepare the report."""
"""
Write a function to extract the tabular information from the given URL under the heading By Market Capitalization, and save it to a data frame.
Write a function to transform the data frame by adding columns for Market Capitalization in GBP, EUR, and INR, rounded to 2 decimal places, based on the exchange rate information shared as a CSV file.
Write a function to load the transformed data frame to an output CSV file.
Write a function to load the transformed data frame to an SQL database server as a table.
Write a function to run queries on the database table.
Run the following queries on the database table:
a. Extract the information for the London office, that is Name and MC_GBP_Billion
b. Extract the information for the Berlin office, that is Name and MC_EUR_Billion
c. Extract the information for New Delhi office, that is Name and MC_INR_Billion
Write a function to log the progress of the code.
While executing the data initialization commands and function calls, maintain appropriate log entries. 
Parameter	Value
Code name	banks_project.py
Data URL	https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks
Exchange rate CSV path	https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv
Table Attributes (upon Extraction only)	Name, MC_USD_Billion
Table Attributes (final)	Name, MC_USD_Billion, MC_GBP_Billion, MC_EUR_Billion, MC_INR_Billion
Output CSV Path	./Largest_banks_data.csv
Database name	Banks.db
Table name	Largest_banks
Log file	code_log.txt
"""
import requests 
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3
import numpy as np
##url = requests.get('https://en.wikipedia.org/wiki/List_of_largest_banks')
##print(url.headers['content-type'])##text/html; charset=UTF-8. This can be extracted as html or text.
url = requests.get('https://en.wikipedia.org/wiki/List_of_largest_banks').text
page = BeautifulSoup(url,'html.parser')

##print(page.prettify())##used to display the structure of the html 

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open("./code_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')
def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    soup = requests.get(url).text
    page = BeautifulSoup(soup,'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    table = page.find_all('tbody')
    rows = table[0].find_all('tr')
    row = 1
    for row in rows:
        col = row.find_all('td')
        if len(col)!= 0:
            tag_a = col[1].find_all('a')
            if len(tag_a) > 1 and tag_a[1] is not None:
                name = tag_a[1].text.strip()
               ## print(name)
            elif len(tag_a) == 1 and tag_a[1] is not None:
                name = tag_a[0].text.strip()
            data_dict = {"Name":name, "MC_USD_Billions":col[2].text.strip()}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
    ##print(df)
    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    USD_List = df["MC_USD_Billions"].tolist()
    USD_List = [float("".join(x.split(','))) for x in USD_List] ##converting USD_Billions to float
    df2 = pd.read_csv(csv_path)
    df['MC_EUR_Billions'] = [np.round(x * float(df2['exchange_rate']['EUR']),2) for x in USD_List]# converting to EUR, and to 2df
    df['MC_GBP_Billions'] = [np.round(x * float(df2['exchange_rate']['GBP']),2) for x in USD_List]# converting to EUR, and to 2df
    df['MC_INR_Billions'] = [np.round(x * float(df2['exchange_rate']['INR']),2) for x in USD_List]# converting to EUR, and to 2df
    ##print(df2['exchange_rate']['EUR'])
    ##print(df)
    return df
def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path) #loads transformed data to the file path below

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement1,query_statement2,query_statement3, sql_connection):
    ''' This function runs the query on the database table and
        prints the output on the terminal. Function returns nothing. '''
    ''' Here, you define the required entities and call the relevant
    functions in the correct order to complete the project. Note that this
    portion is not inside any function.'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 

    #Log first query
    query_output = pd.read_sql(query_statement1, sql_connection)
    with open("sql_queries.txt","a") as f: 
        f.write(timestamp + ' : ' + query_statement1 + '\n')
        f.write(str(query_output) + '\n')

    #Log second query
    query_output = pd.read_sql(query_statement2, sql_connection)
    with open("sql_queries.txt","a") as f: 
        f.write(timestamp + ' : ' + query_statement2 + '\n')
        f.write(str(query_output) +'\n')

    #Log third query
    query_output = pd.read_sql(query_statement3, sql_connection)
    with open("sql_queries.txt","a") as f: 
        f.write(timestamp + ' : ' + query_statement3 + '\n')
        f.write(str(query_output) +'\n')

url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ["Name", "MC_USD_Billions"]
db_name = 'Banks.db'
table_name = 'Largest_banks'
csv_path = 'exchange_rate.csv'
output_path = 'Largest_banks_data.csv'
query_statement1 = f"SELECT * from {table_name}"
query_statement2 = f"SELECT AVG(MC_GBP_Billions) FROM {table_name}"
query_statement3 = f"SELECT Name from {table_name} LIMIT 5"

log_progress('Preliminaries complete. Initiating ETL process')
df = extract(url, table_attribs)
log_progress('Data extraction complete. Initiating Transformation process')
df = transform(df, csv_path)
log_progress('Data transformation complete. Initiating loading process')
load_to_csv(df, output_path)
log_progress('Data saved to CSV file')
sql_connection = sqlite3.connect(db_name)
log_progress('SQL Connection initiated.')
load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as table. Running the query')
query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
run_query(query_statement1,query_statement2,query_statement3, sql_connection)
log_progress('Process Complete.')
sql_connection.close()
