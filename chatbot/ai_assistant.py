"""
This module provides classes for conducting automated interviews and
generating feedback using AI models.

It includes the following classes:

*   `Assistant`: Manages the interview process, handling speech-to-text,
    text-to-speech, and conversational AI responses.

*   `FeedbackAssistant`: Generates feedback on candidate answers,
    utilizing AI models to evaluate responses based on provided criteria,
    job descriptions, and scoring weights.

The module leverages external libraries such as
`openai`, `edge_tts`, `datetime`, `json`, and `re` for AI interactions,
text-to-speech conversion, date/time management, JSON handling, and regular
expressions. It also utilizes environment variables for API keys and settings.
"""

import os
import re
import time
import json
from datetime import datetime, timedelta
from openai import OpenAI, RateLimitError
import edge_tts


# Load environment variables if env.py exists
if os.path.isfile('env.py'):
    import env


class Assistant:
    """
    A class to manage and conduct automated interviews using AI.

    This class handles speech-to-text conversion, text-to-speech conversion,
    and generation of conversational AI responses for a structured interview.

    :param ai_provider: The AI provider to use ('groq' or 'openai').
    Defaults to 'groq'.
    :type ai_provider: str, optional
    :param language: The language of the interview. Defaults to 'en'.
    :type language: str, optional
    :param name: The name of the assistant. Defaults to 'Emma'.
    :type name: str, optional
    :param voice: The voice to use for text-to-speech.
    Defaults to 'en-US-EmmaMultilingualNeural'.
    :type voice: str, optional
    :param interview_duration: The duration of the interview in minutes.
    Defaults to 15.
    :type interview_duration: int, optional
    :param job_post: An object containing job post information
    (title, company_name, description, responsibilities, requirements).
    Defaults to None.
    :type job_post: object, optional
    :param questions_list: A list of custom questions to ask.
    Defaults to None.
    :type questions_list: list, optional
    :param candidate_profile: A dictionary containing candidate information
    (name, key_skills). Defaults to None.
    :type candidate_profile: dict, optional
    """

    def __init__(
            self,
            ai_provider='groq',
            language='en',
            name='Emma',
            voice='en-US-EmmaMultilingualNeural',
            interview_duration=None,
            job_post=None,
            questions_list=None,
            candidate_profile=None
    ):
        """Initialize the Assistant with API key and language settings."""
        self.voice = voice
        self.stt_model = None
        self.chat_model = None
        self.initial_timestamp = datetime.now()
        self.language = language
        self.interview_duration = interview_duration or 15
        self.questions_list = questions_list
        self.candidate_profile = candidate_profile
        self.client = OpenAI()
        self.job_post = job_post
        self.initialize_provider(ai_provider)
        self.system_message = (
            f"You are a professional interview assistant. Your name is "
            f"{name}. Guide the conversation through a structured interview "
            f"progression, starting with an introduction, followed by "
            f"technical questions, behavioral questions,  and concluding "
            f"remarks. You can hear and respond in voice, mimicking natural "
            f"human interaction. Ensure all questions and answers are phrased "
            f"clearly and professionally, without slang, informal phrases, or "
            f"unprofessional language. Your responses must be concise and "
            f"conversational. Avoid using markdown or formatting in your "
            f"replies. The interview started at "
            f"{self.initial_timestamp.strftime('%Y-%m-%d %H:%M:%S')}. Use the "
            f"timestamps in the user's messages to manage the interview flow "
            f"and ensure it is completed within {self.interview_duration} "
            f"minutes. In your initial response, mention the duration of the "
            f"interview and set expectations for the flow. Afterward, do not "
            f"mention the remaining time in every response unless it is "
            f"necessary to guide the pace or alert the user to a time "
            f"constraint for the current section."
        )
        self.update_system_message_with_job_data()
        self.chat_history = [{
                'role': 'system',
                'content': self.system_message
            }]

    def initialize_provider(self, provider):
        """Initialize AI models based on provider like OpenAI or Groq

        :param provider: The AI provider to use ('groq' or 'openai').
        :type provider: str
        """

        if provider == 'groq':
            self.client.base_url = 'https://api.groq.com/openai/v1'
            self.client.api_key = os.environ.get('GROQ_API_KEY')
            self.stt_model = 'whisper-large-v3'
            self.chat_model = os.environ.get('GROQ_MODEL')
        elif provider == 'openai':
            self.client.api_key = os.environ.get('OPENAI_API_KEY')
            self.stt_model = 'whisper-1'
            self.chat_model = 'gpt-4o-mini'


    def get_remaining_time(self):
        """Calculate the remaining interview time.

        :return: A dictionary containing the current timestamp and the
        remaining interview time in minutes.
        :rtype: dict
        """

        current_timestamp = datetime.now()
        elapsed_time = current_timestamp - self.initial_timestamp
        time_left = timedelta(minutes=self.interview_duration) - elapsed_time
        time_left_minutes = max(time_left.total_seconds() // 60, 0)
        return {
            'current_timestamp': current_timestamp.strftime('%Y-%m-%d %H:%M'),
            'time_left': int(time_left_minutes)
        }

    def update_system_message_with_job_data(self):
        """Updates the system message with job and candidate details.

        This method includes job description, responsibilities, and
        requirements, as well as any custom questions and candidate profile
        information into the system message to enhance interview relevance and
        personalization.
        """

        if self.job_post:
            self.system_message += (
                f"You are interviewing a candidate for the position of "
                f"{self.job_post.title} at {self.job_post.company_name}. "
                f"Tailor your technical questions based on the job "
                f"description, which includes: {self.job_post.description}. "
                f"Consider the key responsibilities: "
                f"{self.job_post.responsibilities} and the required skills: "
                f"{self.job_post.requirements}."
            )
        if self.questions_list:
            self.system_message += (
                f"In addition to the standard interview progression, "
                f"ask the following custom questions, selected randomly: "
                f"{', '.join(self.questions_list)}. Make sure all questions "
                f"are asked and that the order is random."
            )

        if self.candidate_profile:
            self.system_message += (
                f"The candidate's profile is as follows:\n"
                f"  - Name: {self.candidate_profile.get('name', 'N/A')}\n"
                f"  - Key Skills: "
                f"{self.candidate_profile.get('key_skills', 'N/A')}\n"
                f"Use this information to personalize the interview "
                f"questions and to assess the candidate's fit for the role."
            )

    def speech_to_text(self, audio_file):
        """Convert speech to text using OpenAI's Whisper model.

        :param audio_file: The audio file to transcribe.
        :type audio_file: file
        :return: The transcribed text.
        :rtype: str
        """

        try:
            transcription = self.client.audio.transcriptions.create(
                model=self.stt_model,
                language=self.language,
                file=audio_file
            )
            return transcription.text
        except Exception as e:
            return f'Error in speech_to_text: {e}'

    def openai_chat(self, text: str):
        """Generate chat responses using OpenAI's GPT model.

        :param text: The user input text.
        :type text: str
        :yield: A stream of text chunks as generated by the chat model.
        :rtype: generator of str
        """

        time_data = self.get_remaining_time()
        current_time = time_data.get('current_timestamp')
        remaining_time = time_data.get('time_left')

        self.chat_history.append({
            'role': 'user',
            'content': (
                f'{text} | timestamp: {current_time}, '
                f'remaining: {remaining_time} minutes.'
            )
        })
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
        except RateLimitError as _:
            yield from [
                "I'm sorry, but you have reached the Assistant usage limit.",
                "Please try again later.",
                "Thank you for your patience!"
            ]
        except Exception as _:
            yield from [
                "An error occurred.",
                "Please try again later.",
                "Thank you for your patience!"
            ]

    async def text_to_speech(self, text: str):
        """Convert text to speech using Edge TTS.

        :param text: The text to convert to speech.
        :type text: str
        :return: The audio bytes.
        :rtype: bytes
        """

        try:
            communicate = edge_tts.Communicate(text, voice=self.voice)
            audios = []
            async for chunk in communicate.stream():
                if chunk['type'] == 'audio':
                    audios.append(chunk['data'])
            return b''.join(audios)
        except Exception as e:
            return f'Error in text_to_speech: {e}'

    def stream_to_sentences(self, stream):
        """Split a stream of text into sentences.

        :param stream: The text stream.
        :type stream: generator of str
        :yield: The individual sentences from the stream.
        :rtype: generator of str
        """

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


class FeedbackAssistant:
    """
    A class to provide feedback on candidate answers during job interviews.

    This class utilizes AI models to evaluate candidate responses based on
    provided evaluation criteria, job descriptions, and scoring weights.
    It ensures all scores are between 0 and 100.

    :param ai_provider: The AI provider to use ('groq' or 'openai').
    Defaults to 'groq'.
    :type ai_provider: str, optional
    :param language: The language of the feedback. Defaults to 'en'.
    :type language: str, optional
    :param job_post: An object containing job post information
    (title, company_name, description, responsibilities, requirements).
    Defaults to None.
    :type job_post: object, optional
    :param evaluation_criteria: A list of dictionaries containing
    evaluation criteria with weights and scoring guides. Defaults to None.
    :type evaluation_criteria: list, optional
    """

    def __init__(
            self, ai_provider='groq',
            language='en',
            job_post=None,
            evaluation_criteria=None
    ):
        self.chat_model = None
        self.language = language
        self.job_post = job_post
        self.evaluation_criteria = evaluation_criteria
        self.client = OpenAI()
        self.initialize_provider(ai_provider)
        self.system_message = self.generate_system_message()

    def initialize_provider(self, provider):
        """Initialize AI models based on provider like OpenAI or Groq

        :param provider: The AI provider to use ('groq' or 'openai').
        :type provider: str
        """

        if provider == 'groq':
            self.client.base_url = 'https://api.groq.com/openai/v1'
            self.client.api_key = os.environ.get('GROQ_API_KEY')
            self.chat_model = os.environ.get('GROQ_MODEL')
        elif provider == 'openai':
            self.client.api_key = os.environ.get('OPENAI_API_KEY')
            self.chat_model = 'gpt-4o-mini'

    def generate_system_message(self):
        """Generate a system message for evaluating candidate answers,
        ensuring scores are between 0 and 100.

        The system message includes the job description, responsibilities,
        required skills, and the evaluation criteria with scoring guides.
        It ensures that the feedback is provided in a specific JSON format
        with scores between 0 and 100.

        :return: The generated system message.
        :rtype: str
        """

        system_message = (
            f"You are a structured assistant designed to evaluate candidate "
            f"answers during a job interview. Analyze the responses and "
            f"provide feedback in JSON format based on the evaluation "
            f"criteria, job description, and scoring weights. **All scores "
            f"you provide must be in the range of 0 to 100, inclusive.**"
            f"\n\nThe interview is for the position of {self.job_post.title} "
            f"at {self.job_post.company_name}. The job description includes: "
            f"{self.job_post.description}. Key responsibilities are: "
            f"{self.job_post.responsibilities}. Required skills include: "
            f"{self.job_post.requirements}.\n\nEvaluation criteria to "
            f"consider during feedback:"
        )

        for idx, criterion in enumerate(self.evaluation_criteria, start=1):
            system_message += (
                f"\n  {idx}. {criterion['criterion']} "
                f"(Weight: {criterion['weight']}%). "
                f"Scoring guide: {criterion['scoring_guide']}."
            )

        system_message += (
            "\n\nYour JSON output must strictly follow this structure:"
            "\n{"
            "\n  '<criterion_1_name>': {"
            "\n    'score': <numerical_score>,  "
            "// **Score must be between 0 and 100**"
            "\n    'comment': '<feedback>',"
            "\n    'weight': <weight>"
            "\n  },"
            "\n  '<criterion_2_name>': {"
            "\n    'score': <numerical_score>,  "
            "// **Score must be between 0 and 100**"
            "\n    'comment': '<feedback>',"
            "\n    'weight': <weight>"
            "\n  },"
            "\n  ... (repeat for all criteria)"
            "\n  'overall_score': <weighted_average_score>, "
            "// **This should also be between 0 and 100**"
            "\n  'recommendation': '<summary_of_candidate_potential_and_fit>'"
            "\n  'feedback': '<summarize_candidate_fit_for_the_position_and_provide_specific_constructive_suggestions_for_improvement>'"
            "\n}"
        )
        return system_message

    def generate_feedback(self, text: str, max_retries=3, initial_delay=1):
        """Generate chat responses using OpenAI's GPT model or Groq model.

        This method will try multiple times if the feedback is not generated
        in the correct JSON format.

        :param text: The user input text (candidate answer).
        :type text: str
        :param max_retries: The maximum number of retries. Defaults to 3.
        :type max_retries: int, optional
        :param initial_delay: The initial delay (in seconds)
        before the first retry. Defaults to 1.
        :type initial_delay: int, optional
        :return: The generated feedback in JSON format.
        :rtype: dict or None
        """

        message = [
            {'role': 'system', 'content': self.system_message},
            {'role': 'user', 'content': text}
        ]

        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.chat_model,
                    response_format={'type': 'json_object'},
                    messages=message,
                )
                content = completion.choices[0].message.content
                return json.loads(content)
            except json.JSONDecodeError as _:
                if attempt < max_retries - 1:
                    delay = initial_delay * (2 ** attempt)
                    time.sleep(delay)
                else:
                    return None
            except Exception as _:
                return None

        # Return a default empty dictionary if no successful feedback
        return {}
