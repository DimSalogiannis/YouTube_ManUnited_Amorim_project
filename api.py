import pandas as pd
import seaborn as sns
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("youtube_api_key")
youtube = build('youtube', 'v3', developerKey = api_key)

# search parameters of the data
QUERY = 'Manchester United'
START_DATE = '2024-08-11T00:00:00Z'
END_DATE = datetime.now(timezone.utc).isoformat("T") + "Z"
MAX_RESULTS = 50 # maximum number of results to return 
DAILY_LIMIT = 10000 # maximum number of requests per day
API_COST_PER_CALL = 100

# the following code snippet is used to read the date that the previous request stopped at and continue from there,  
# ensuring that no data is lost or duplicated in the process
try:
    with open('last_date.txt', 'r') as f:
        last_date = f.read().strip()
        if last_date:
            START_DATE = last_date
except FileNotFoundError:
    pass

def get_video_data(start_date, end_date):
    all_videos_ids = []
    next_page_token = None
    api_calls = 0
    
    while True:
        if api_calls >= DAILY_LIMIT / API_COST_PER_CALL:
            break
        
    request = youtube.search().list(
        part = 'snippet',
        q = QUERY, 
        type = 'video',
        maxResults = MAX_RESULTS,
        publishedAfter = start_date,
        publishedBefore = end_date,
        pageToke = next_page_token
    )
    response = request.execure()
    api_calls += 1
    
    