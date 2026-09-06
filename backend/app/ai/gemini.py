import logging
import os
from pathlib import Path

from google import genai

logger = logging.getLogger(__name__)

# C:\NEXUS_ONE\backend\app\ai\gemini.py
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"


def load_nexus_env():
    """
    Directly read NEXUS ONE .env.
    This avoids python-dotenv parsing/path issues.
    """

    if not ENV_FILE.exists():
        raise RuntimeError(
            f"NEXUS ONE .env not found: {ENV_FILE}"
        )

    for raw_line in ENV_FILE.read_text(
        encoding="utf-8-sig"
    ).splitlines():

        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "=" not in line:
            continue

        name, value = line.split("=", 1)

        name = name.strip()
        value = value.strip()

        if name and value:
            os.environ[name] = value


def get_gemini_client():

    load_nexus_env()

    api_key = os.environ.get(
        "GEMINI_API_KEY",
        ""
    ).strip()

    if not api_key:
        raise RuntimeError(
            f"GEMINI_API_KEY is not configured. "
            f"ENV FILE: {ENV_FILE}"
        )

    logger.info(
        "Gemini API key loaded successfully."
    )

    return genai.Client(
        api_key=api_key
    )


def ask_gemini(prompt: str) -> str:

    try:

        client = get_gemini_client()

        if len(prompt) > 12000:
            prompt = prompt[:12000]

        load_nexus_env()

        model = os.environ.get(
            "GEMINI_MODEL",
            "gemini-flash-lite-latest"
        ).strip()

        if not model or "=" in model:
            model = "gemini-flash-lite-latest"

        logger.info(
            "Gemini model: %s",
            model
        )

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        text = getattr(
            response,
            "text",
            None
        )

        if text:
            return text.strip()

        return "No response generated."

    except Exception as e:

        error_text = str(e)

        logger.exception(
            "Gemini error encountered"
        )

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):
            return "GEMINI_QUOTA_EXCEEDED"

        if (
            "API key" in error_text
            or "api_key" in error_text.lower()
            or "401" in error_text
            or "403" in error_text
            or "authentication" in error_text.lower()
        ):
            return "GEMINI_AUTH_ERROR"

        return "GEMINI_SERVICE_ERROR"
