import io
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .ai_assistant import Assistant, FeedbackAssistant
from .model_managers import DatabaseManager
import asyncio
import pdfplumber



class VoiceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_post = None
        self.criteria = None
        self.preparation = None
        self.assistant = None

    async def connect(self):
        """Initialize an Assistant instance for this WebSocket connection."""
        try:
            await self.initialize_interview()
            await self.accept()
        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        """Handle disconnection."""
        asyncio.create_task(self.generate_feedback_on_disconnect())

    async def receive(self, text_data=None, bytes_data=None):
        """Process received data from WebSocket."""
        if bytes_data:
            await self.process_voice_data(bytes_data)

        await self.send(text_data=json.dumps({'message': 'Data received'}))

    async def initialize_interview(self):
        """Initialize interview parameters and assistant."""
        db_manager = DatabaseManager(self.scope)
        self.job_post = await db_manager.get_job_post()
        self.criteria = await db_manager.get_evaluation_criteria()
        self.preparation = await db_manager.get_interview_preparation()
        self._create_assistant()
        candidate_resume = db_manager.get_candidate_resume(user_id=2)
        print(candidate_resume)
        # self.read_to_text(candidate_resume)


    def _create_assistant(self):
        """Create an Assistant instance based on preparation details."""
        assistant_params = {
            'ai_provider': 'groq',
            'job_post': self.job_post,
        }

        if self.preparation:
            assistant_params.update({
                'interview_duration': self.preparation.get('interview_duration'),
                'questions_list': self.preparation.get('questions')
            })

        self.assistant = Assistant(**assistant_params)

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


    def read_to_text(self, pdf_file):
        audio_buffer = io.BytesIO(pdf_file)
        audio_buffer.name = 'test.pdf'
        # audio_buffer.seek(0)

        with pdfplumber.open(audio_buffer) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()

            print(text)