import requests
import os
from dotenv import load_dotenv
from time import sleep
import json

from assemblyai import assemblyAI


load_dotenv()

API_KEY = os.getenv("API_KEY")

aai = assemblyAI(API_KEY)

audio_url = "https://s3-us-west-2.amazonaws.com/blog.assemblyai.com/audio/8-7-2018-post/7510.mp3"

data = aai.get_full_transcription(audio_url)

print(json.dumps(data, indent=4))

