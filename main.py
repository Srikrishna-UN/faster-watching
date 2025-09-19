import os
from dotenv import load_dotenv
import googleapiclient.discovery
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from docx import Document

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
PLAYLIST_ID = os.getenv('PLAYLIST_ID')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OUTPUT_PATH = os.getenv('OUTPUT_PATH')
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT')

# --- CONSTANTS ---
SUMMARY_FILE_NAME = 'Faster watching'
LAST_VIDEO_FILE = 'last_processed_video.txt'

# --- API CLIENTS ---
youtube = googleapiclient.discovery.build(
    'youtube', 'v3', developerKey=YOUTUBE_API_KEY
)

genai.configure(api_key=GEMINI_API_KEY)

# --- CORE FUNCTIONS ---

def get_new_videos():
    """Fetches new video IDs from the playlist by comparing against the last processed video."""
    try:
        with open(LAST_VIDEO_FILE, 'r') as f:
            last_video_id = f.read().strip()
    except FileNotFoundError:
        last_video_id = None

    new_videos = []
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=PLAYLIST_ID,
        maxResults=50
    )
    response = request.execute()

    for item in response['items']:
        video_id = item['snippet']['resourceId']['videoId']
        if video_id == last_video_id:
            break
        new_videos.append(
            {
                'id': video_id,
                'title': item['snippet']['title']
            }
        )
    new_videos.reverse()
    if new_videos:
        with open(LAST_VIDEO_FILE, 'w') as f:
            f.write(new_videos[-1]['id'])

    return new_videos


def get_transcript(video_id):
    """Fetches the transcript for a given video ID using youtube-transcript-api."""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        raw_data = transcript.to_raw_data()
        full_text = " ".join([d['text'] for d in raw_data])
        return full_text
    except Exception as e:
        print(f"Could not get transcript for video {video_id}: {e}")
        return None


def summarize_with_gemini(transcript):
    """Summarizes the transcript using the Gemini 2.5 Flash model."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
You are a highly effective summarization assistant. I will provide a full video transcript. Your tasks are:

Write a concise, objective summary of the video's main ideas (no opinions, no unnecessary detail).

Provide a bulleted list of actionable takeaways — specific lessons, tips, or steps a viewer could apply right away.

Keep the summary concise and short unless the transcript is unusually long. Ensure the takeaways are clear, practical, and phrased so they can be implemented directly.

{transcript}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

# --- FILE WRITING FUNCTIONS ---

def write_markdown_file(video_title, video_url, summary, counter):
    """Appends a new summary to a single markdown note."""
    filepath = os.path.join(OUTPUT_PATH, f"{SUMMARY_FILE_NAME}.md")
    content = f"""
---
### {counter}. {video_title}
**[Watch on YouTube]({video_url})**

{summary}

"""
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully appended summary to: {filepath}")


def write_docx_file(video_title, video_url, summary, counter):
    """Appends a new summary to a single DOCX document."""
    filepath = os.path.join(OUTPUT_PATH, f"{SUMMARY_FILE_NAME}.docx")
    
    # Check if the file exists; if not, create a new document
    if not os.path.exists(filepath):
        doc = Document()
    else:
        doc = Document(filepath)

    doc.add_heading(f"{counter}. {video_title}", level=2)
    doc.add_paragraph(f"Watch on YouTube: {video_url}")
    
    # Add summary content line by line
    for line in summary.splitlines():
        # Handle bullet points
        if line.strip().startswith(('*', '-', '+')):
            doc.add_paragraph(line.strip().lstrip('*-+').strip(), style='List Bullet')
        else:
            doc.add_paragraph(line)
    
    doc.add_page_break()
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    doc.save(filepath)
    print(f"Successfully appended summary to: {filepath}")

def write_txt_file(video_title, video_url, summary, counter):
    """Appends a new summary to a single plain text document."""
    filepath = os.path.join(OUTPUT_PATH, f"{SUMMARY_FILE_NAME}.txt")
    content = f"""
---
{counter}. {video_title}
Watch on YouTube: {video_url}

{summary}

"""
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully appended summary to: {filepath}")

def main():
    """Main function to run the entire workflow."""
    print("Checking for new videos...")
    new_videos = get_new_videos()

    if not new_videos:
        print("No new videos found.")
        return

    counter = 1 

    for video in new_videos:
        video_id = video['id']
        video_title = video['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"Processing video: {video_title} ({video_url})")

        transcript = get_transcript(video_id)
        if transcript:
            summary = summarize_with_gemini(transcript)
            if summary:
                if OUTPUT_FORMAT == 'md':
                    write_markdown_file(video_title, video_url, summary, counter)
                elif OUTPUT_FORMAT == 'docx':
                    write_docx_file(video_title, video_url, summary, counter)
                elif OUTPUT_FORMAT == 'txt':
                    write_txt_file(video_title, video_url, summary, counter)
                else:
                    print(f"Error: Invalid OUTPUT_FORMAT specified in .env: {OUTPUT_FORMAT}")
                    break
                counter += 1
            else:
                print("Failed to generate summary.")
        else:
            print("Skipping due to failed transcript retrieval.")

if __name__ == "__main__":
    main()
