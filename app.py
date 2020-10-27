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
        while True:
            if self.state == JohnState.DEFAULT:
                self.recognize_speech_from_mic()


    def handleResponse(self, recognizer, audio):
        try:
            self.handleTranscription(recognizer.recognize_google(audio))
        except sr.UnknownValueError:
            print("I did not understand. Please repeat.")
        except sr.RequestError:
            print("It would appear that my brain is fried. I can not handle your request.")
        

    def handleTranscription(self, transcription):
        if (transcription == None):
            pass
        if self.state == JohnState.WAITING_CALL and transcription == 'hey John':
            self.state = JohnState.LISTENING_ACTION
            print('Hello. What can I do for you?')
        elif self.state == JohnState.LISTENING_ACTION:
            print('You told me this: {0}'.format(transcription))
            self.state = JohnState.WAITING_CALL


    def recognize_speech_from_mic(self):
        self.state = JohnState.WAITING_CALL
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        self.recognizer.listen_in_background(
            self.microphone,
            self.handleResponse
        )


if __name__ == "__main__":
    r = sr.Recognizer()
    mic = sr.Microphone()
    john = John(r, mic)
    john.listen()
