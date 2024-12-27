import os
import io
import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import edge_tts

# Load environment variables if env.py exists
if os.path.isfile('env.py'):
    import env


class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Initialize an Assistant instance for this WebSocket connection."""
        self.assistant = Assistant(ai_provider='groq')
        await self.accept()

    async def disconnect(self, close_code):
        """Handle disconnection."""
        pass

    async def receive(self, text_data=None, bytes_data=None):
        """Process received data from WebSocket."""
        if bytes_data:
            await self.process_voice_data(bytes_data)

        await self.send(text_data=json.dumps({'message': 'Data received'}))

    async def process_voice_data(self, bytes_data):
        """Process the voice data received from WebRTC."""
        audio_buffer = io.BytesIO(bytes_data)
        audio_buffer.name = 'speech.ogg'
        audio_buffer.seek(0)

        if text := self.assistant.speech_to_text(audio_buffer).strip():
            text_stream = self.assistant.openai_chat(text)
            sentences = self.assistant.stream_to_sentences(text_stream)

            for sentence in sentences:
                audio_data = await self.assistant.text_to_speech(sentence)
                if audio_data:
                    await self.send(bytes_data=audio_data)


class Assistant:
    def __init__(self, ai_provider='groq', language='en'):
        """Initialize the Assistant with API key and language settings."""
        self.stt_model = None
        self.chat_model = None
        self.language = language
        self.client = OpenAI()
        self.initialize_provider(ai_provider)
        self.system_message = (
            "You are a professional interview assistant. Your name is Sarah. Guide "
            "the conversation through a structured interview progression, starting "
            "with an introduction, followed by technical questions, behavioral "
            "questions, and concluding remarks. You can hear and respond in voice, "
            "mimicking natural human interaction. Ensure all questions and answers "
            "are phrased clearly and professionally, without slang, informal "
            "phrases, or unprofessional language. Your responses must be concise "
            "and conversational. Avoid using markdown or formatting in your replies."
        )
        self.chat_history = [{'role': 'system', 'content': self.system_message}]

    def initialize_provider(self, provider):
        """Initialize AI models based on provider like OpenAI or Groq"""
        if provider == 'groq':
            self.client.base_url = 'https://api.groq.com/openai/v1'
            self.client.api_key = os.environ.get('GROQ_API_KEY')
            self.stt_model = 'whisper-large-v3'
            self.chat_model = 'llama-3.3-70b-specdec'
        elif provider == 'openai':
            self.client.api_key = os.environ.get('OPENAI_API_KEY')
            self.stt_model = 'whisper-1'
            self.chat_model = 'gpt-4o-mini'

    def speech_to_text(self, audio_file):
        """Convert speech to text using OpenAI's Whisper model."""
        try:
            transcription = self.client.audio.transcriptions.create(
                model=self.stt_model,
                language=self.language,
                file=audio_file
            )
            return transcription.text
        except Exception as e:
            print(f'Error in speech_to_text: {e}')
            return ''

    def openai_chat(self, text: str):
        """Generate chat responses using OpenAI's GPT model."""
        self.chat_history.append({'role': 'user', 'content': text})
        self.chat_history.append({'role': 'assistant', 'content': ''})

        try:
            for chunk in self.client.chat.completions.create(
                    model=self.chat_model,
                    messages=self.chat_history,
                    stream=True
            ):
                if (text_chunk := chunk.choices[0].delta.content) is not None:
                    self.chat_history[-1]['content'] += text_chunk
                    yield text_chunk
        except Exception as e:
            print(f'Error in openai_chat: {e}')

    async def text_to_speech(self, text: str):
        """Convert text to speech using Edge TTS."""
        try:
            communicate = edge_tts.Communicate(text)
            audios = []
            async for chunk in communicate.stream():
                if chunk['type'] == 'audio':
                    audios.append(chunk['data'])
            return b''.join(audios)
        except Exception as e:
            print(f'Error in text_to_speech: {e}')
            return None

    def stream_to_sentences(self, stream):
        """Split a stream of text into sentences."""
        buffer = ''
        sentence_endings = re.compile(r'[.!?]')

        for chunk in stream:
            buffer += chunk
            while True:
                match = sentence_endings.search(buffer)
                if not match:
                    break
                sentence_end = match.end()
                sentence = buffer[:sentence_end].strip()
                buffer = buffer[sentence_end:]
                if sentence:
                    yield sentence

        if buffer.strip():
            yield buffer.strip()
