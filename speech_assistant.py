import threading
import time
import speech_recognition as sr
import pyttsx3
import queue
import rag
from gigachat_rag import GigaRAG

class SpeechAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.text_queue = queue.Queue()  # Очередь для передачи текста между потоками
        self.stop_listening = False
        self.is_speaking = False  # Флаг для отслеживания воспроизведения голоса

    def listen_and_recognize(self):
        """Поток для распознавания речи."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Слушаю...")
            while not self.stop_listening:
                if not self.is_speaking:  # Если идет воспроизведение голоса, пропускаем цикл
                    try:
                        #self.recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio = self.recognizer.listen(source, timeout=2)
                        recognized_text = self.recognizer.recognize_google(audio, language="ru-RU")
                        if self.is_speaking:
                            recognized_text = ""
                        print(f"Распознано: {recognized_text}")
                        if(len(recognized_text)>2):
                            self.text_queue.put(recognized_text)  # Добавляем распознанный текст в очередь
                        if "стоп" in recognized_text.lower():
                            self.stop_listening = True
                            break
                    except sr.WaitTimeoutError:
                        if not self.text_queue.empty():
                            print("Пауза в речи, отправка текста на обработку")
                            self.is_speaking = True  # Устанавливаем флаг воспроизведения
                            self.process_text()
                    except sr.UnknownValueError:
                        print("Речь не распознана")
                    except sr.RequestError:
                        print("Ошибка сервиса распознавания")

    def process_text(self):
        """Функция обработки текста."""
        text = ""
        while not self.text_queue.empty():
            text += self.text_queue.get()
        # Пример обработки текста (можно заменить на свою логику)
        print("generate response")
        #processed_text = self.rag_system.generate_response(text, max_length=200)
        processed_text = self.rag_system.ask_chain(text)
        #processed_text = deepseek.chat_stream(text)  - Если использовать бесплатный API
        print(f"Обработанный текст: {processed_text}")
        self.speak(processed_text)

    def speak(self, text):
        """Синтез речи."""
        self.is_speaking = True  # Устанавливаем флаг воспроизведения
        self.engine.say(text)
        self.engine.runAndWait()  # Ждем завершения воспроизведения
        self.is_speaking = False  # Сбрасываем флаг после завершения


    def init_rag(self):
        # Инициализация RAG
        #self.rag_system = rag.RAG()
        self.rag_system = GigaRAG()
        self.rag_system.load_database()
        self.rag_system.create_qa_chain()

    def run(self):
        print("init rag")
        self.init_rag()
        """Запуск потоков."""
        listen_thread = threading.Thread(target=self.listen_and_recognize)
        listen_thread.start()
        # Основной цикл для обработки текста и синтеза речи
        try:
            while not self.stop_listening:
                if not self.text_queue.empty():
                    self.process_text()
                time.sleep(0.1)  # Небольшая задержка, чтобы не нагружать CPU
        except KeyboardInterrupt:
            print("Приложение завершено.")
        finally:
            self.stop_listening = True
            listen_thread.join()


if __name__ == "__main__":
    assistant = SpeechAssistant()
    assistant.run()