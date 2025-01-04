import io
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from .ai_assistant import Assistant


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
        history = self.assistant.chat_history
        res = '\n'.join(f'{": ".join(message.values())}'.split('|')[0] for message in history[1:])
        print(res)


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



