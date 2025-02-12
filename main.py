from main_frame import MainFrame
import tkinter as Tk
import rag
from speech_assistant import SpeechAssistant
import deepseek
from gigachat_rag import GigaRAG

def start():
    root = Tk.Tk()
    mf = MainFrame(root)
    root.mainloop()


if __name__ == "__main__":
    assistant = SpeechAssistant()
    assistant.run()
    #start()
    #print(deepseek.chat_stream("Сочини сказку на ночь"))
    #rag = GigaRAG()
    #rag.test3()