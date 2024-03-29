#----------------Imports----------------
from dotenv import load_dotenv
import os
import pandas as pd
import ApiHandler 
from sqlalchemy import create_engine
import urllib
import sys
#----------------Imports----------------

#----------------Initialize----------------
load_dotenv()
server = os.getenv("DB_SERVER_NAME")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
driver= '{ODBC Driver 18 for SQL Server}' # Hier den Treiber entsprechend anpassen

# Erstelle die Verbindungszeichenkette
conn_str = f'DRIVER={driver};SERVER=tcp:{server},1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# Formattiere den Connection String für SQLAlchemy
params = urllib.parse.quote_plus(conn_str)
conn_str_formatted = 'mssql+pyodbc:///?odbc_connect={}'.format(params)

#Baue Engine
engine_azure = create_engine(conn_str_formatted,echo=True)
print('connection is ok')
#----------------Initialize----------------

#----------------Functions----------------
def saveMostPopularVideosByCountryCH():
    df = ApiHandler.getMostPopularVideosByCountry('CH', 50)
    # DataFrame in SQL-Tabelle einfügen
    df.to_sql('mostpopularvideosbycountry', con=engine_azure, index=False, if_exists='append', chunksize=100)
    print("Einfügen abgeschlossen")

def saveMostPopularVideosByCountryGeneric(countryCode, limit):
    df = ApiHandler.getMostPopularVideosByCountry(countryCode, limit)
    # DataFrame in SQL-Tabelle einfügen
    df.to_sql('mostpopularvideosbycountry', con=engine_azure, index=False, if_exists='append', chunksize=100)
    print("Einfügen abgeschlossen")

def getMostPopularVideosByCountryCH():
    # SQL-Abfrage definieren
    query = "SELECT * FROM [dbo].[mostpopularvideosbycountry] WHERE Country_Chart = 'CH'"

    # Führe die Abfrage aus und speichere das Ergebnis in einem DataFrame
    df = pd.read_sql(query, con=engine_azure)
    return df  

def getMostPopularVideosByCountryGeneric(countryCode):
    # SQL-Abfrage definieren
    query = f"SELECT * FROM [dbo].[mostpopularvideosbycountry] WHERE Country_Chart = \'{countryCode}\'"

    # Führe die Abfrage aus und speichere das Ergebnis in einem DataFrame
    df = pd.read_sql(query, con=engine_azure)
    return df  

def getMostPopularVideosByCountryAll():
    # SQL-Abfrage definieren
    query = f"SELECT * FROM [dbo].[mostpopularvideosbycountry]"

    # Führe die Abfrage aus und speichere das Ergebnis in einem DataFrame
    df = pd.read_sql(query, con=engine_azure)
    return df 

def getCountByCategoriesFilterByCountry(countryCode):
    # SQL-Abfrage definieren
    query = f"SELECT Category_Name, COUNT(*) as Count FROM [dbo].[mostpopularvideosbycountry] WHERE Country_Chart = \'{countryCode}\' GROUP BY Category_Name"

    # Führe die Abfrage aus und speichere das Ergebnis in einem DataFrame
    df = pd.read_sql(query, con=engine_azure)
    return df 

def getAverageStatCountByCategoryFilterByCountry(countryCode):
    # SQL-Abfrage definieren
    query = f"SELECT Category_Name, avg(Views) as Avg_Views, avg(Like_Count) as Avg_Likes, avg(Comment_Count) as Avg_Comments FROM [dbo].[mostpopularvideosbycountry] WHERE Country_Chart = \'{countryCode}\' GROUP BY Category_Name"

    # Führe die Abfrage aus und speichere das Ergebnis in einem DataFrame
    df = pd.read_sql(query, con=engine_azure)
    return df 
#----------------Functions---------------- 

