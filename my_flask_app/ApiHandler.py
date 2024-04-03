#----------------Imports----------------
from googleapiclient.discovery import build
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
import re
import isodate
#----------------Imports----------------

#----------------Initialize----------------
load_dotenv()
localDevKey = os.environ["DEVELOPER_KEY"]
youtube_api = build('youtube', 'v3', developerKey=localDevKey)
#----------------Initialize----------------

#----------------Functions----------------
# Funktion, um Emojis aus einem String zu entfernen
def remove_emojis(text):
    # Regulärer Ausdruck, der Nicht-ASCII-Zeichen, einschließlich Emojis, findet
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbole & Piktogramme
        u"\U0001F680-\U0001F6FF"  # Transport & Karte
        u"\U0001F1E0-\U0001F1FF"  # Flaggen (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"  
        "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', text)

def get_channel_subscriber_count(channel_id):
    request = youtube_api.channels().list(
        part='statistics',
        id=channel_id
    )
    response = request.execute()
    if 'items' in response:
        statistics = response['items'][0]['statistics']
        if 'subscriberCount' in statistics:
            return int(statistics['subscriberCount'])
    return None


def getMostPopularVideosByCountry(pRegionCode, pNumOfRecords):
    # Anfrage an die YouTube Data API, um die populärsten Videos in der Schweiz zu erhalten
    request = youtube_api.videos().list(
        part='snippet,statistics,contentDetails',  # Du kannst mehr Teile hinzufügen, je nach benötigten Informationen
        chart='mostPopular',
        regionCode=pRegionCode,  # Setze den Region-Code auf CH für die Schweiz
        maxResults=pNumOfRecords  # Anzahl der Ergebnisse, die zurückgegeben werden sollen (max. 50)
    )

    # Kategorien Mapping
    category_request = youtube_api.videoCategories().list(
        part='snippet',
        regionCode='CH'  # Setzen Sie den gleichen Region-Code ein, den Sie auch vorher verwendet haben
    )

    # Requests ausführen um Resultate zu erhalten
    response = request.execute()
    category_response = category_request.execute()

    # Mapping von categoryId zu Kategorienamen erstellen
    category_mapping = {item['id']: item['snippet']['title'] for item in category_response.get('items', [])}

    # Leere Liste erstellen für Resultset
    responseData = []

    # Durchlaufe die Antwort und extrahiere die gewünschten Informationen
    for video in response.get('items', []):
        chartCountry = pRegionCode
        title = video['snippet']['title']
        description = video['snippet']['description']
        #tags = video['snippet'].get('tags', [])
        publishedAt = video['snippet']['publishedAt']
        channelid = video['snippet']['channelId']
        channeltitle = video['snippet']['channelTitle']
        categoryid = video['snippet']['categoryId']
        category_name = category_mapping.get(categoryid, "Unbekannte Kategorie")  # Kategorienamen aus dem Mapping holen
        duration = isodate.parse_duration(video['contentDetails']['duration']).total_seconds()
        definition = video['contentDetails']['definition']
        projection = video['contentDetails']['projection']
        views = video['statistics']['viewCount']
        likeCount = video['statistics'].get('likeCount', 0)  # Standardwert, falls nicht vorhanden
        commentCount = video['statistics'].get('commentCount', 0)  # Standardwert, falls nicht vorhanden
        extractionDate = datetime.today().strftime('%Y-%m-%d')

        # Abonnentenanzahl für den Kanal abrufen
        subscriber_count = get_channel_subscriber_count(channelid)

        responseData.append([chartCountry, remove_emojis(title), remove_emojis(description), publishedAt, channelid, channeltitle, category_name, duration, definition, projection, views, likeCount, commentCount, extractionDate, subscriber_count])
    
    # Erstelle einen DataFrame aus der Liste    
    df = pd.DataFrame(responseData, columns=['Country_Chart', 'Title', 'Description', 'Published_At', 'Channel_ID', 'Channel_Title', 'Category_Name', 'Duration', 'Definition', 'Projection', 'Views', 'Like_Count', 'Comment_Count', 'Extraction_Date', 'Subscriber_Count'])
    
    # Konvertierung von 'Published_At' und 'Extraction_Date' in datetime64
    df['Published_At'] = pd.to_datetime(df['Published_At']).dt.tz_localize(None)

    # Konvertierung der Datentypen
    df = df.astype({
        'Country_Chart': 'string',
        'Title': 'string',
        'Description': 'string',
        'Published_At': 'datetime64[ns]',
        'Channel_ID': 'string',
        'Channel_Title': 'string',
        'Category_Name': 'string',
        'Duration': 'int64',  # oder 'int', abhängig davon, ob Sie Sekunden als ganze Zahlen speichern möchten
        'Definition': 'category',  # Kategorische Daten für 'HD', 'SD' usw.
        'Projection': 'category',  # Ebenfalls kategorisch, da wahrscheinlich nur wenige Werte vorhanden sind
        'Views': 'int64',
        'Like_Count': 'int64',
        'Comment_Count': 'int64',
        'Extraction_Date': 'datetime64[ns]',
        'Subscriber_Count': 'Int64'  # 'Int64', um fehlende Werte darzustellen
    })

    return df
#----------------Functions----------------

