import requests
import base64
import io

from observation_settings import is_observation_enabled

OLLAMA_URL = "http://localhost:11434/api/generate"
VISION_MODEL = "qwen2.5vl:3b"


def analyze_screen(screenshot):

    if not is_observation_enabled():
        return None

    if screenshot is None:
        return None

    try:
        image_buffer = io.BytesIO()
        screenshot.save(image_buffer, format="PNG")

        image_base64 = base64.b64encode(
            image_buffer.getvalue()
        ).decode("utf-8")

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": VISION_MODEL,
                "prompt": """
                Analyze the visible computer screen.

                Identify:
                1. Active application and page.
                2. Visible text and headings.
                3. Important buttons and UI elements.
                4. Errors or warnings.
                5. What the user appears to be viewing.

                Describe only what is visibly supported.
                Do not click anything or execute commands.
                """,
                "images": [image_base64],
                "stream": False,
                "think": False,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0.2,
                    "num_predict": 400
                }
            },
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result.get("response", "").strip() or None

    except requests.exceptions.RequestException as error:
        print("Screen Analysis Network Error:", error)
        return None

    except Exception as error:
        print("Screen Analysis Error:", error)
        return None