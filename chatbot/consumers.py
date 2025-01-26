"""
This module contains the VoiceConsumer WebSocket consumer for handling
voice-based interactions in an interview setting. It connects to a WebSocket,
processes incoming voice data, and interacts with an AI assistant to assist in
interviews. The consumer also generates feedback at the end of the session and
handles audio conversion between speech-to-text and text-to-speech.

It integrates with the Assistant and FeedbackAssistant classes to handle
AI-powered conversations, and interacts with the DatabaseManager to manage
job-related data, evaluation criteria, and user profiles.

Modules:
    io: For handling audio data in memory.
    json: For processing and sending JSON messages via WebSocket.
    channels.generic.websocket: For WebSocket consumer base class.
    .ai_assistant: For managing AI-based assistant interactions.
    .model_managers: For managing database interactions.
    asyncio: For asynchronous task management.

Classes:
    VoiceConsumer: A WebSocket consumer for managing voice interactions
    in an interview.
"""

import io
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .ai_assistant import Assistant, FeedbackAssistant
from .model_managers import DatabaseManager


class VoiceConsumer(AsyncWebsocketConsumer):
    """
    A WebSocket consumer for handling voice-based interactions in an interview.

    This class manages the WebSocket connection, processes voice data,
    and generates feedback after the interview session.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the VoiceConsumer instance.

        Sets up the initial state, including job post, criteria, user profile,
        assistant, and database manager.
        """

        super().__init__(*args, **kwargs)
        self.job_post = None
        self.criteria = None
        self.preparation = None
        self.is_candidate = False
        self.user_profile = None
        self.assistant = None
        self.db_manager = None
        self.is_staff = False

    async def connect(self):
        """
        Handle the WebSocket connection.

        Initializes the interview parameters and accepts the connection.
        """

        try:
            await self.initialize_interview()
            await self.accept()
        except Exception as _:
            await self.close()

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.

        Generates feedback for the user when disconnecting after the interview.
        """

        if not self.is_candidate:
            return

        asyncio.create_task(self.generate_feedback_on_disconnect())

    async def receive(self, text_data=None, bytes_data=None):
        """
        Handle received data from the WebSocket.

        Processes either text or voice data and sends a response back
        to the client.

        :param text_data: The text data received from the WebSocket.
        :param bytes_data: The bytes data (audio) received from the WebSocket.
        """

        if bytes_data:
            await self.process_voice_data(bytes_data)

        await self.send(text_data=json.dumps({'message': 'Data received'}))

    async def initialize_interview(self):
        """
        Initialize the interview parameters and assistant.

        Retrieves data from the database, including job post,
        evaluation criteria, interview preparation details, and user profile.
        It also sets up the assistant.
        """

        self.db_manager = DatabaseManager(self.scope)
        self.job_post = await self.db_manager.get_job_post()
        self.criteria = await self.db_manager.get_evaluation_criteria()
        self.preparation = await self.db_manager.get_interview_preparation()
        self.is_candidate = await self.db_manager.is_candidate()
        self.is_staff = await self.db_manager.is_staff()

        if self.is_candidate:
            self.user_profile = await self.db_manager.get_user_profile()

        self._create_assistant()

    def _create_assistant(self):
        """
        Create and initialize the Assistant instance based on the preparation
        details.

        The assistant is created using parameters based on whether the user is
        a candidate or staff member, and additional details from the interview
        preparation or user profile.
        """

        assistant_params = {
            'ai_provider': 'openai' if self.is_staff else 'groq',
            'job_post': self.job_post,
        }

        if self.preparation:
            assistant_params.update({
                'interview_duration': self.preparation.get(
                    'interview_duration'),
                'questions_list': self.preparation.get('questions')
            })

        if speaker := self.scope['session'].get('speaker'):
            assistant_params.update(speaker)

        if self.user_profile:
            assistant_params.update({'candidate_profile': self.user_profile})

        self.assistant = Assistant(**assistant_params)

    async def generate_feedback_on_disconnect(self):
        """
        Generate and handle feedback upon disconnection.

        If there is sufficient conversation history, generate feedback and
        send it to both the user (candidate) and the employer.
        """

        conversation_history = self.assistant.chat_history
        if len(conversation_history) >= 4:
            conversation_text = '\n'.join(
                f"{': '.join(message.values())}".split('|', maxsplit=1)[0]
                for message in conversation_history[1:]
            )
            feedback_assistant = FeedbackAssistant(
                ai_provider='openai' if self.is_staff else 'groq',
                job_post=self.job_post,
                evaluation_criteria=self.criteria
            )
            feedback = feedback_assistant.generate_feedback(conversation_text)

            if feedback:
                await self.db_manager.send_feedback_to_user(
                    job_title=self.job_post.title,
                    company_name=self.job_post.company_name,
                    feedback=feedback.get('feedback')
                )
                await self.db_manager.send_feedback_to_employer(feedback)


    async def process_voice_data(self, bytes_data):
        """
        Process the voice data received from WebRTC.

        Converts speech data to text, sends it to the assistant for processing,
        and returns audio responses.

        :param bytes_data: The raw audio data received from the WebSocket.
        """

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
