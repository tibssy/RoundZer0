from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import json
import os
import io
if os.path.isfile('env.py'):
    import env


LANGUAGE = 'en'
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Process the voice data received from WebRTC
            audio_buffer = io.BytesIO(bytes_data)
            audio_buffer.name = 'speech.ogg'
            audio_buffer.seek(0)

            text = self.speech_to_text(audio_buffer)

            print(f"Received voice data: {len(bytes_data)} bytes. Text: {text}")
        await self.send(text_data=json.dumps({"message": "Data received"}))

    def speech_to_text(self, audio_file):
        """Convert audio to text using OpenAI's API."""
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        transcription = openai_client.audio.transcriptions.create(
            model="whisper-1",
            language=LANGUAGE,
            file=audio_file
        )

        print(transcription)
        return transcription.text