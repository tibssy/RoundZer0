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
            f"You are a professional interview assistant. Your name is {name}. Guide "
            f"the conversation through a structured interview progression, starting "
            f"with an introduction, followed by technical questions, behavioral "
            f"questions,  and concluding remarks. You can hear and respond in voice, "
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
            self.chat_model = os.environ.get('GROQ_MODEL')
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
        if self.questions_list:
            self.system_message += (
                f"In addition to the standard interview progression, ask the following "
                f"custom questions, selected randomly: {', '.join(self.questions_list)}. "
                f"Make sure all questions are asked and that the order is random."
            )

        if self.candidate_profile:
            self.system_message += (
                f"The candidate's profile is as follows:\n"
                f"  - Name: {self.candidate_profile.get('name', 'N/A')}\n"
                f"  - Key Skills: {self.candidate_profile.get('key_skills', 'N/A')}\n"
                f"Use this information to personalize the interview questions and to assess the candidate's fit for the role."
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
        except RateLimitError as e:
            return (
                "I'm sorry, but you have reached the Assistant usage limit.",
                "Please try again later.",
                "Thank you for your patience!"
            )
        except Exception as e:
            return (
                "An error occurred.",
                "Please try again later.",
                "Thank you for your patience!"
            )

    async def text_to_speech(self, text: str):
        """Convert text to speech using Edge TTS."""
        try:
            communicate = edge_tts.Communicate(text, voice=self.voice)
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


class FeedbackAssistant:
    def __init__(self, ai_provider='groq', language='en', job_post=None, evaluation_criteria=None):
        self.chat_model = None
        self.language = language
        self.job_post = job_post
        self.evaluation_criteria = evaluation_criteria
        self.client = OpenAI()
        self.initialize_provider(ai_provider)
        self.system_message = self.generate_system_message()

    def initialize_provider(self, provider):
        """Initialize AI models based on provider like OpenAI or Groq"""
        if provider == 'groq':
            self.client.base_url = 'https://api.groq.com/openai/v1'
            self.client.api_key = os.environ.get('GROQ_API_KEY')
            self.chat_model = 'llama-3.3-70b-versatile'
        elif provider == 'openai':
            self.client.api_key = os.environ.get('OPENAI_API_KEY')
            self.chat_model = 'gpt-4o-mini'

    def generate_system_message(self):
        """Generate a system message for evaluating candidate answers, ensuring scores are between 0 and 100."""
        system_message = (
            f"You are a structured assistant designed to evaluate candidate answers during a job interview. "
            f"Analyze the responses and provide feedback in JSON format based on the evaluation criteria, job description, and scoring weights. "
            f"**All scores you provide must be in the range of 0 to 100, inclusive.**"
            f"\n\nThe interview is for the position of {self.job_post.title} at {self.job_post.company_name}. "
            f"The job description includes: {self.job_post.description}. "
            f"Key responsibilities are: {self.job_post.responsibilities}. "
            f"Required skills include: {self.job_post.requirements}."
            f"\n\nEvaluation criteria to consider during feedback:"
        )

        for idx, criterion in enumerate(self.evaluation_criteria, start=1):
            system_message += (
                f"\n  {idx}. {criterion['criterion']} (Weight: {criterion['weight']}%). "
                f"Scoring guide: {criterion['scoring_guide']}."
            )

        system_message += (
            "\n\nYour JSON output must strictly follow this structure:"
            "\n{"
            "\n  '<criterion_1_name>': {"
            "\n    'score': <numerical_score>,  // **Score must be between 0 and 100**"
            "\n    'comment': '<feedback>',"
            "\n    'weight': <weight>"
            "\n  },"
            "\n  '<criterion_2_name>': {"
            "\n    'score': <numerical_score>,  // **Score must be between 0 and 100**"
            "\n    'comment': '<feedback>',"
            "\n    'weight': <weight>"
            "\n  },"
            "\n  ... (repeat for all criteria)"
            "\n  'overall_score': <weighted_average_score>, // **This should also be between 0 and 100**"
            "\n  'recommendation': '<summary_of_candidate_potential_and_fit>'"
            "\n  'feedback': '<summarize_candidate_fit_for_the_position_and_provide_specific_constructive_suggestions_for_improvement>'"
            "\n}"
        )
        return system_message

    def generate_feedback(self, text: str, max_retries=3, initial_delay=1):
        """Generate chat responses using OpenAI's GPT model."""
        message = [
            {'role': 'system', 'content': self.system_message},
            {'role': 'user', 'content': text}
        ]

        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.chat_model,
                    response_format={"type": "json_object"},
                    messages=message,
                )
                content = completion.choices[0].message.content
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f"Attempt {attempt + 1}/{max_retries} - JSONDecodeError: {e}")
                if attempt < max_retries - 1:
                    delay = initial_delay * (2 ** attempt)
                    print(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    print("Max retries reached. Could not parse JSON.")
                    return None
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries} - Error in generate_feedback: {e}")
                return None
