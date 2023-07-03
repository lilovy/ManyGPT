import poe
import json
from poe import Client
from enum import Enum


class LlmModels(Enum):
    ChatGPT = "chinchilla"
    Sage = "capybara"
    GPT4 = "beaver"
    PaLM = "acouchy"
    Claude = "a2"

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
        model: LlmModels = LlmModels.Sage,
        flush: bool = False,
    ):
        model = model.value
        for chunk in self._client.send_message(model, message):
            if flush:
                yield chunk["text_new"]
        # if not flush:
        #     return chunk["text"]


if __name__ == "__main__":
    client = LLMs("o6BvUBrXYXuis5Xb5Y1CLg%3D%3D")
    ask = client.ask("hi, how a u?", flush=True)
    for i in ask:
        print(i, end="", flush=True)