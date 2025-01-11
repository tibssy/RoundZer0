import random


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

def get_assistant():
    return random.choice(tuple(VOICES.items()))