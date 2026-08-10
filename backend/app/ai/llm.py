import logging

from app.ai.groq import GroqLLM

logger = logging.getLogger(__name__)


class HybridLLM:
    """
    Groq is the primary and currently active LLM.
    Gemini fallback is disabled to avoid quota-related failures.
    """

    def invoke(self, prompt: str):

        class Response:
            def __init__(self, text):
                self.content = text

        try:
            groq = GroqLLM()
            result = groq.invoke(prompt)

            if result and result.content:
                logger.debug("LLM Provider: GROQ")
                return Response(result.content)

            raise RuntimeError("Groq returned an empty response.")

        except Exception as error:
            logger.exception("Groq failed")
            raise RuntimeError("LLM invocation failed")


def get_llm():
    return HybridLLM()
