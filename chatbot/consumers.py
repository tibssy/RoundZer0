import os
import io
import json
import re
from datetime import datetime, timedelta
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import edge_tts
from urllib.parse import parse_qs
from channels.db import database_sync_to_async


# Load environment variables if env.py exists
if os.path.isfile('env.py'):
    import env


class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Initialize an Assistant instance for this WebSocket connection."""
        job_post = None

        if job_post_id := self.get_job_id():
            try:
                from jobposts.models import JobPost
                job_post = await database_sync_to_async(JobPost.objects.get)(pk=job_post_id)
            except JobPost.DoesNotExist:
                print(f"JobPost with ID {job_post_id} not found.")
                await self.close()
                return


        self.assistant = Assistant(ai_provider='groq', interview_duration=10, job_post=job_post)
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


    def get_job_id(self):
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        job_post_id_list = query_params.get('job_post_id', [])
        return job_post_id_list[0] if job_post_id_list else None


class Assistant:
    def __init__(self, ai_provider='groq', language='en', interview_duration=30, job_post=None):
        """Initialize the Assistant with API key and language settings."""
        self.stt_model = None
        self.chat_model = None
        self.initial_timestamp = datetime.now()
        self.language = language
        self.interview_duration = interview_duration
        self.client = OpenAI()
        self.job_post = job_post
        self.initialize_provider(ai_provider)
        self.system_message = (
            f"You are a professional interview assistant. Your name is Sarah. Guide "
            f"the conversation through a structured interview progression, starting "
            f"with an introduction, followed by technical questions, behavioral "
            f"questions, and concluding remarks. You can hear and respond in voice, "
            f"mimicking natural human interaction. Ensure all questions and answers "
            f"are phrased clearly and professionally, without slang, informal "
            f"phrases, or unprofessional language. Your responses must be concise "
            f"and conversational. Avoid using markdown or formatting in your replies. "
            f"The interview started at {self.initial_timestamp.strftime('%Y-%m-%d %H:%M:%S')}. "
            f"Use the timestamps in the user's messages to manage the interview flow "
            f"and ensure it is completed within {self.interview_duration} minutes. "
            f"In your initial response, mention the duration of the interview and "
            f"set expectations for the flow. Afterward, do not mention the remaining time "
            f"in every response unless it is necessary to guide the pace or alert the user "
            f"to a time constraint for the current section."
        )
        self.update_system_message_with_job_data()
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


    def get_remaining_time(self):
        current_timestamp = datetime.now()
        elapsed_time = current_timestamp - self.initial_timestamp
        time_left = timedelta(minutes=self.interview_duration) - elapsed_time
        time_left_minutes = max(time_left.total_seconds() // 60, 0)
        return {
            'current_timestamp': current_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'time_left': int(time_left_minutes)
        }

    def update_system_message_with_job_data(self):
        if self.job_post:
            self.system_message += (
                f"You are interviewing a candidate for the position of {self.job_post.title} "
                f"at {self.job_post.company_name}. Tailor your technical questions based "
                f"on the job description, which includes: {self.job_post.description}. Consider "
                f"the key responsibilities: {self.job_post.responsibilities} and the required "
                f"skills: {self.job_post.requirements}."
            )

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
        time_data = self.get_remaining_time()
        current_time = time_data.get('current_timestamp')
        remaining_time = time_data.get('time_left')

        self.chat_history.append({
            'role': 'user',
            'content': f'{text} | timestamp: {current_time}, remaining: {remaining_time} minutes.'}
        )
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
