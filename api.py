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

