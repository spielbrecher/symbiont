import speech_recognition as sr

class SpeechRecognizer:

    def __init__(self):
        # Инициализация распознавания речи
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.input_text = ''

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_thread = self.root.after(100, self.listen)

    def stop_listening(self):
        if self.listening:
            self.listening = False
            self.root.after_cancel(self.listen_thread)

    def listen(self):
        if self.listening:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio, language="ru-RU")
                    self.input_text += text + "\n"
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
            self.listen_thread = self.root.after(100, self.listen)