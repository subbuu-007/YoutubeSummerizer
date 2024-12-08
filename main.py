import os
import openai
from googleapiclient.discovery import build
import youtube_dl
from transformers import pipeline

# Set up the YouTube API client
API_KEY = 'AIzaSyCH3-6JcKS5YZVGCyKH60TJfywkc3eOm3U'  # Replace with your API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Function to fetch video details
def get_video_details(video_id):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    
    # Extract video details
    video_details = response['items'][0]
    title = video_details['snippet']['title']
    description = video_details['snippet']['description']
    view_count = video_details['statistics']['viewCount']
    
    return title, description, view_count

# Function to download video audio using youtube-dl
def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',  # Save audio as 'audio.mp4' or 'audio.webm'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Function to transcribe audio to text using OpenAI's Whisper or Google Speech-to-Text
def transcribe_audio():
    # Use openai's Whisper model (as an example, requires API key for OpenAI)
    openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key
    
    with open("audio.mp4", "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
    return transcript['text']

# Function to summarize text using HuggingFace's transformers
def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Main function to summarize a YouTube video
def summarize_youtube_video(video_url):
    video_id = video_url.split("v=")[-1]  # Extract video ID from URL
    title, description, view_count = get_video_details(video_id)
    
    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"View Count: {view_count}")
    
    # Download audio from YouTube video
    print("Downloading audio...")
    download_audio(video_url)
    
    # Transcribe audio to text
    print("Transcribing audio...")
    transcript = transcribe_audio()
    
    # Summarize the transcript
    print("Summarizing transcript...")
    summary = summarize_text(transcript)
    
    return summary

# Example usage:
video_url = "https://www.youtube.com/watch?v=VIDEO_ID"  # Replace with actual video URL
summary = summarize_youtube_video(video_url)
print("\nVideo Summary:")
print(summary)
