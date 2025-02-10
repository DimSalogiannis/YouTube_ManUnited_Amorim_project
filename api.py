import pandas as pd
import seaborn as sns
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import time
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

# the following function is used to get the video data from the youutube API using the search parameters
def get_video_data(start_date, end_date):
    all_videos_ids = []
    next_page_token = None
    api_calls = 0
    
    while True:
        if api_calls >= DAILY_LIMIT / API_COST_PER_CALL:
            break
          
        # snippet to make the request to the youtube API
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
        
        # snippet to get the video id and the published dates from the response
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            published_date = item['snippet']['publishedAt']
            all_videos_ids.append((video_id, published_date))
            
            
        next_page_token = response.get('nextPageToken')
        
        if not next_page_token:
            break
    
    return all_videos_ids

# calling the function to get the video data
videos_ids_dates = get_video_data(START_DATE, END_DATE)


# sace the last date of the request to a file 
if videos_ids_dates:
    last_date = videos_ids_dates[-1][1] 
    with open('last_date.txt', 'w') as f:
        f.write(last_date)
        
        
# the following function is used to get video details 
def get_video_details(video_ids):
    video_stats = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part = 'snippet, statistics',
            id = ','.join(video_ids[i:i+50])
        )
        response = request.execute()
        
        for item in response.get('items', []):
            video_stats.append({
                'videoId': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channelTitle': item['snippet']['channelTitle'],
                'publishedAt': item['snippet']['publishedAt'],
                'viewCount': item['statistics'].get('viewCount', 0),
                'likeCount': item['statistics'].get('likeCount', 0),
                'tags': item['snippet'].get('tags', []),
                'categoryId': item['snippet']['categoryId']
            })
                
        time.sleep(1)
        
    return video_stats

video_ids = [video[0] for video in videos_ids_dates]

videos_details = get_video_details(video_ids)