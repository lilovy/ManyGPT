import poe
import json
from poe import Client
from enum import Enum
from config import token, proxy


class LlmModels(Enum):
    ChatGPT = "chinchilla"
    Claude = "a2"
    Sage = "capybara"
    # GPT4 = "beaver"
    # PaLM = "acouchy"

class LLMs(object):
    def __init__(self, token: str, proxy: str = None):
        self._client = Client(token, proxy=proxy)

    def _models(self):
        return json.dumps(
            self._client.bot_names,
            indent=4
        )

    def ask(
        self,
        message: str,
        model: str = "chinchilla",
        flush: bool = False,
    ):
        content = self._client.send_message(model, message)

        for chunk in content:
            if flush:
                yield chunk["text_new"]
        yield chunk["text"]
    
    def new_bot(
        self,
        name: str,
        prompt: str,
        base_model: str,
    ):
        bot = self._client.create_bot(
            name,
            prompt,
            base_model,
            prompt_public=False,
            
        )
        return bot


def get_llm():
    llm = LLMs(token, proxy)
    yield llm

if __name__ == "__main__":
    client = LLMs("o6BvUBrXYXuis5Xb5Y1CLg%3D%3D")
    ask = client.ask("hi, how a u?", flush=True)
    for i in ask:
        print(i, end="", flush=True)