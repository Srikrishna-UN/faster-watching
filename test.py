import os
from dotenv import load_dotenv
import googleapiclient.discovery
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from docx import Document


load_dotenv()

PLAYLIST_ID = os.getenv('PLAYLIST_ID')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OUTPUT_PATH = os.getenv('OUTPUT_PATH')
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT')
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
request = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=PLAYLIST_ID,
            maxResults=50,
        )
response = request.execute()
print(response)