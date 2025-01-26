"""
Voice assistant configuration and helper function.

This module contains a dictionary of available voices for the chatbot
along with their corresponding language codes. It also provides a helper
function `get_assistant()` that randomly selects and returns a voice
from the dictionary, which can be used for voice-related interactions
in the chatbot.
"""

from typing import Tuple
import random


# Dictionary mapping assistant names to their corresponding voice codes
VOICES = {
    'Connor': 'en-IE-ConnorNeural',
    'Emily': 'en-IE-EmilyNeural',
    'Ava': 'en-US-AvaMultilingualNeural',
    'Andrew': 'en-US-AndrewMultilingualNeural',
    'Emma': 'en-US-EmmaMultilingualNeural',
    'Brian': 'en-US-BrianMultilingualNeural',
    'Libby': 'en-GB-LibbyNeural',
    'Ryan': 'en-GB-RyanNeural',
    'Sonia': 'en-GB-SoniaNeural',
    'Aria': 'en-US-AriaNeural',
    'Christopher': 'en-US-ChristopherNeural',
    'Eric': 'en-US-EricNeural',
    'Jenny': 'en-US-JennyNeural',
    'Michelle': 'en-US-MichelleNeural',
    'Roger': 'en-US-RogerNeural',
    'Steffan': 'en-US-SteffanNeural',
    'Clara': 'en-CA-ClaraNeural',
    'Natasha': 'en-AU-NatashaNeural',
    'Liam': 'en-CA-LiamNeural',
    'William': 'en-AU-WilliamNeural'
}

def get_assistant() -> Tuple[str, str]:
    """
    Randomly selects and returns a voice assistant.

    The function chooses a random voice from the VOICES dictionary and returns
    a tuple containing the assistant's name and the corresponding voice code.

    :return: A tuple containing the assistant's name and voice code.
    :rtype: tuple
    """

    return random.choice(tuple(VOICES.items()))
