from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import json
import os
import io
if os.path.isfile('env.py'):
    import env


LANGUAGE = 'en'
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
SYSTEM_MESSAGE = "You are a professional interview assistant. Respond with clear and professional questions and answers"


class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Initialize an Assistant instance for this WebSocket connection
        self.assistant = Assistant(api_key=OPENAI_API_KEY, language=LANGUAGE)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):

        if bytes_data:
            # Process the voice data received from WebRTC
            audio_buffer = io.BytesIO(bytes_data)
            audio_buffer.name = 'speech.ogg'
            audio_buffer.seek(0)

            text = self.assistant.speech_to_text(audio_buffer)
            print(f"Received voice data: {len(bytes_data)} bytes.\n\nText: {text}")

            self.assistant.openai_chat(text)

        await self.send(text_data=json.dumps({"message": "Data received"}))


class Assistant:
    def __init__(self, api_key, base_url = None, language='en'):
        self.api_key = api_key
        self.language = language
        self.client = OpenAI(api_key=self.api_key)
        if base_url:
            self.client.base_url = base_url

        self.chat_history = [{"role": "system", "content": SYSTEM_MESSAGE}]

    def speech_to_text(self, audio_file):
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            language=self.language,
            file=audio_file
        )
        return transcription.text

    def openai_chat(self, text: str):
        self.chat_history.append({'role': 'user', 'content': text})
        self.chat_history.append({'role': 'assistant', 'content': ''})

        for chunk in self.client.chat.completions.create(
                model='gpt-4o-mini',
                messages=self.chat_history,
                stream=True
        ):
            if (text_chunk := chunk.choices[0].delta.content) is not None:
                print(text_chunk, end='', flush=True)
                self.chat_history[-1]['content'] += text_chunk
                # yield text_chunk