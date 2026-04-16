from google import genai
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Model constants
GEMINI_3_PRO = "gemini-3-pro-preview"
GEMINI_3_FLASH = "gemini-3-flash-preview"
GEMINI_3_PRO_IMAGE = "gemini-3-pro-image-preview"


def get_client(api_key: Optional[str] = None) -> genai.Client:
    """
    Initialize and return a Gemini API client.

    Args:
        api_key: Optional API key. If not provided, will use GEMINI_API_KEY env var.

    Returns:
        genai.Client instance
    """
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError(
                "API key must be provided either as parameter or GEMINI_API_KEY environment variable"
            )

    return genai.Client(api_key=api_key)


def generate_text(
    prompt: str,
    client: genai.Client,
    model: str = GEMINI_3_FLASH,
) -> str:
    """
    Generate text response from a prompt (simplified interface).

    Args:
        prompt: Text prompt
        model: Model to use

    Returns:
        Generated text as string
    """

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
    )
    return response.text
