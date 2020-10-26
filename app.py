import speech_recognition as sr
from enum import Enum

class JohnState(Enum):
    DEFAULT = None
    WAITING_CALL = 1
    LISTENING_ACTION = 2

class John:

    state = JohnState.DEFAULT

    def __init__(self, recognizer, microphone):

        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        self.recognizer = recognizer
        self.microphone = microphone

    def listen(self):
        print("Greetings! I'm John and I'm at your service.")
        self.state = JohnState.WAITING_CALL
        while True:
            if self.state == JohnState.DEFAULT:
                break

            response = self.recognize_speech_from_mic()
            self.handleResponse(response)


    def handleResponse(self, response):
        transcription = response['transcription']
        if (transcription == None):
            self.handleNoTranscription()
        elif (transcription == 'hey John'):
            self.state = JohnState.LISTENING_ACTION
            print('Hello, Mikael. What can I do for you?')
        else:
            self.state = JohnState.WAITING_CALL
            print('You told me this: {0}'.format(transcription))
        
    def handleNoTranscription(self):
        if (self.state == JohnState.WAITING_CALL):
            print("Would you please repeat what you said? I couldn't catch that.")

    def recognize_speech_from_mic(self):

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        response = {
            'success': True,
            'error': None,
            'transcription': None
        }

        try:
            response['transcription'] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            response['success'] = False
            response['error'] = 'API unavailable'
        except sr.UnknownValueError:
            response['error'] = 'Unable to recognize speech'

        return response

if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone()
    john = John(r, mic)
    john.listen()
