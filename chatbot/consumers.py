import io
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .ai_assistant import Assistant, FeedbackAssistant
from .model_managers import DatabaseManager
import asyncio


class VoiceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_post = None
        self.criteria = None
        self.assistant = None

    async def connect(self):
        """Initialize an Assistant instance for this WebSocket connection."""
        try:
            await self.initialize_interview()
        except Exception as e:
            await self.close()
            return
        await self.accept()

    async def disconnect(self, close_code):
        """Handle disconnection."""
        asyncio.create_task(self.generate_feedback_on_disconnect())

    async def receive(self, text_data=None, bytes_data=None):
        """Process received data from WebSocket."""
        if bytes_data:
            await self.process_voice_data(bytes_data)

        await self.send(text_data=json.dumps({'message': 'Data received'}))

    async def initialize_interview(self):
        db_manager = DatabaseManager(self.scope)
        self.job_post = await db_manager.get_job_post()
        self.criteria = await db_manager.get_evaluation_criteria()
        preparation_details = await db_manager.get_interview_preparation()
        interview_duration = preparation_details.get('interview_duration')
        questions = preparation_details.get('questions')
        self.assistant = Assistant(
            ai_provider='groq',
            interview_duration=interview_duration,
            job_post=self.job_post,
            questions_list=questions
        )

    async def generate_feedback_on_disconnect(self):
        """Generate and handle feedback upon disconnection."""
        conversation_history = self.assistant.chat_history
        if len(conversation_history) >= 4:
            conversation_text = '\n'.join(
                f'{": ".join(message.values())}'.split('|')[0]
                for message in conversation_history[1:]
            )
            feedback_assistant = FeedbackAssistant(
                job_post=self.job_post,
                evaluation_criteria=self.criteria
            )
            feedback = feedback_assistant.generate_feedback(conversation_text)
            print(feedback)
            # Send feedback to employer and a brief result to candidate...

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