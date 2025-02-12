from langchain.callbacks.base import BaseCallbackHandler


class StreamHandler(BaseCallbackHandler):
    def __init__(self, initial_text=""):
        pass

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"{token} -", end="", flush=True)