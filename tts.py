from gtts import gTTS
import os


class TTS:
    text: str
    language: str

    def __init__(self):
        pass

    def set_text(self, text):
        self.text = text

    def set_language(self, language):
        self.language = language

    def text_to_speech(self, filename):
        tts = gTTS(text=self.text, lang=self.language)
        tts.save(filename)

    def play_file(self, filename):
        os.system("mpg321 "+filename)