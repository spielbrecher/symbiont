import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import rag
import threading

class MainFrame:

    def __init__(self, root):
        self.root = root
        self.root.title("Symbiont v. 1")

        # Создание полей для ввода и вывода текста
        self.input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.input_text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.output_text.grid(row=0, column=2, padx=10, pady=10, columnspan=2)

        # Создание кнопок
        self.start_listen_button = tk.Button(root, text="Старт прослушивания", command=self.thread_listening)
        self.start_listen_button.grid(row=1, column=0, padx=5, pady=10)

        self.stop_listen_button = tk.Button(root, text="Стоп прослушивания", command=self.stop_listening)
        self.stop_listen_button.grid(row=1, column=1, padx=5, pady=10)

        self.start_speak_button = tk.Button(root, text="Старт озвучивания", command=self.thread_speaking)
        self.start_speak_button.grid(row=1, column=2, padx=5, pady=10)

        self.stop_speak_button = tk.Button(root, text="Стоп озвучивания", command=self.stop_speaking)
        self.stop_speak_button.grid(row=1, column=3, padx=5, pady=10)

        # Инициализация распознавания речи
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False

        # Инициализация синтеза речи
        self.engine = pyttsx3.init()
        self.speaking = False

        # Инициализация RAG
        self.rag_system = rag.RAG()

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_thread = self.root.after(10, self.listen)

    def stop_listening(self):
        if self.listening:
            self.listening = False
            self.root.after_cancel(self.listen_thread)
        # answer
        answer = self.rag_answer(self.input_text.get(1.0, tk.END), max_length=0)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, answer)
        self.start_speaking()

    def listen(self):
        if self.listening:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio, language="ru-RU")
                    self.input_text.insert(tk.END, text + "\n")
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
            #self.listen_thread = self.root.after(10, self.listen)

    def start_speaking(self):
        if not self.speaking:
            self.speaking = True
            self.engine = pyttsx3.init()
            text = self.output_text.get("1.0", tk.END)
            print(text)
            self.engine.say(text)
            self.engine.runAndWait()
            self.speaking = False


    def thread_listening(self):
        threading.Thread(target=self.listen, daemon=False).start()

    def thread_speaking(self):
        threading.Thread(target=self.start_speaking, daemon=False).start()

    def stop_speaking(self):
        if self.speaking:
            self.engine.stop()
            self.speaking = False

    def rag_answer(self, prompt, max_length):
        #prompt = "Hi, can you break an easy promt to robot into small set of commands?"
        answer = self.rag_system.generate_response(prompt, max_length=max_length)
        print(answer)
        return answer
