import logging
import os

from dotenv import load_dotenv
from google import genai

logger = logging.getLogger(__name__)

load_dotenv()


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.warning("GEMINI_API_KEY not found in .env")
        raise Exception("GEMINI_API_KEY not found in .env")

    return genai.Client(api_key=api_key)


def ask_gemini(prompt: str) -> str:

    client = get_gemini_client()

    if len(prompt) > 12000:
        prompt = prompt[:12000]

    logger.debug("Gemini request length: %d", len(prompt))

    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "No response generated."

    except Exception as e:

        error_text = str(e)

        logger.error("Gemini error encountered")

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):
            return "GEMINI_QUOTA_EXCEEDED"

        if (
            "API key" in error_text
            or "401" in error_text
            or "403" in error_text
        ):
            return "GEMINI_AUTH_ERROR"

        return "GEMINI_SERVICE_ERROR"
