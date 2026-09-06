import logging

from app.ai.gemini import ask_gemini

logger = logging.getLogger(__name__)


class HybridLLM:
    """
    NEXUS ONE LLM provider.

    Gemini is the active provider.
    """

    def invoke(self, prompt: str):

        class Response:
            def __init__(self, text):
                self.content = text

        try:
            result = ask_gemini(prompt)

            if result:
                logger.info("LLM Provider: GEMINI")
                return Response(result)

            raise RuntimeError("Gemini returned an empty response.")

        except Exception:
            logger.exception("Gemini LLM failed")
            raise RuntimeError("LLM invocation failed")


def get_llm():
    return HybridLLM()
