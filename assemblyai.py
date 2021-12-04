import requests
import os
from dotenv import load_dotenv
from time import sleep
import json
import subprocess

load_dotenv()

class assemblyAI():
    """
    A python wrapper for the assemblyai api. https://docs.assemblyai.com/overview/getting-started
    """

    def __init__(self, API_KEY):
        # define api key

        self.API_KEY = API_KEY

    def temp_upload_mp3(self, mp3_file_path):
        """
        Uploads a file to the assemblyai server.  All uploads are immediately deleted after transcription, uploads are not stored.
        """

        filename = mp3_file_path
        
        def read_file(filename, chunk_size=5242880):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data
        
        headers = {'authorization': self.API_KEY}
        response = requests.post('https://api.assemblyai.com/v2/upload',
                                headers=headers,
                                data=read_file(filename))

        print(response.json())

        self.audio_url = response.json().get("upload_url")

        return response.json()

    def temp_upload_mp4(self, mp4_file_path):
        """
        Transcribes an mp4 file into an mp3 file.
        Uploads a file to the assemblyai server.  All uploads are immediately deleted after transcription, uploads are not stored.
        """

        # convert mp4 to mp3 using subprocess
        os.system(f"C:/UserAddedPrograms/ffmpeg-2021-12-02-git-4a6aece703-full_build/bin/ffmpeg -i {mp4_file_path} ./temp.mp3")

        return self.temp_upload_mp3("./temp.mp3")


    def transcribe(self, audio_url=""):
        if audio_url == "" and self.audio_url == "":
            raise Exception("No audio url provided")
        
        if audio_url != "":
            self.audio_url = audio_url

        endpoint = "https://api.assemblyai.com/v2/transcript"

        audio_data = {
        "audio_url": self.audio_url,
        }

        headers = {
            "authorization": self.API_KEY,
            "content-type": "application/json"
        }

        response = requests.post(endpoint, json=audio_data, headers=headers)

        data = response.json()

        self.id = data.get("id")

        #print(json.dumps(data, indent=4))

        return data

    def get_transcription(self):
        """
        Gets the transcription of the audio file. Will return a json object with the partial transcription. 
        Call this function repeatedly until it returns a status of "completed".
        """

        if self.id == "":
            raise Exception("No transcription id provided, please run the transcribe function first")

        headers = {
            "authorization": self.API_KEY,
            "content-type": "application/json"
        }

        endpoint = f"https://api.assemblyai.com/v2/transcript/{self.id}"

        response = requests.get(endpoint, headers=headers)
        
        data2 = response.json()

        #print(json.dumps(data2, indent=4))

        #returns string of transcription
        return data2

    def get_full_transcription(self, audio_url):
        """
        Blocking function. Gets the full transcription of the audio file. Will return a json object with the full transcription. 
        """

        #check if audio url is http
        # if audio_url[4:] != "http":
        #     if audio_url[:3] != "mp3":
        #         audio_url = self.temp_upload_mp3(audio_url)
        #     if audio_url[:3] == "mp4":
        #         audio_url = self.temp_upload_mp4(audio_url)
        
        self.transcribe(audio_url)

        data = []

        while True:
            partial_trancsription = self.get_transcription()
            data.append(partial_trancsription)
            if partial_trancsription.get("status") == "completed":
                break
        
        return data
