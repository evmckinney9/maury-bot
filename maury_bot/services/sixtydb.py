import base64
import io

import aiohttp
from discord import FFmpegPCMAudio
from tenacity import retry, stop_after_attempt, wait_exponential

# 60db text-to-speech endpoint (buffered synthesis, returns base64 audio).
TTS_SYNTHESIZE_URL = "https://api.60db.ai/tts-synthesize"

# Voice tuning. 60db uses a 0-100 scale (ElevenLabs uses 0-1), so these mirror
# the ElevenLabs settings in elevenlabs.py (stability 0.3 -> 30, similarity
# 0.85 -> 85) to keep Captain Maury's delivery consistent across providers.
DEFAULT_STABILITY = 30
DEFAULT_SIMILARITY = 85
DEFAULT_SPEED = 1
DEFAULT_OUTPUT_FORMAT = "mp3"


class SixtyDBAPIError(Exception):
    """Custom exception for 60db API errors."""

    pass


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    reraise=True,
)
async def robust_synthesize(session, headers, payload):
    """POST to the 60db synthesize endpoint with retries on transient errors."""
    async with session.post(
        TTS_SYNTHESIZE_URL, headers=headers, json=payload
    ) as response:
        response.raise_for_status()
        return await response.json()


async def get_sixtydb_audio(bot, message: str):
    bot.logger.info("Generating audio stream (60db)...")
    try:
        headers = {
            "Authorization": f"Bearer {bot.config['sixtydb_api_key']}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": message,
            "voice_id": bot.config["sixtydb_voice_id"],
            "stability": DEFAULT_STABILITY,
            "similarity": DEFAULT_SIMILARITY,
            "speed": DEFAULT_SPEED,
            "output_format": DEFAULT_OUTPUT_FORMAT,
        }

        async with aiohttp.ClientSession() as session:
            result = await robust_synthesize(session, headers, payload)

        if not result.get("success") or not result.get("audio_base64"):
            raise SixtyDBAPIError(
                result.get("message", "60db returned no audio.")
            )

        audio = base64.b64decode(result["audio_base64"])

        # Convert bytes to AudioSource using FFmpegPCMAudio (same as ElevenLabs).
        audio_source = FFmpegPCMAudio(
            executable="ffmpeg", source=io.BytesIO(audio), pipe=True
        )

        return audio_source

    except SixtyDBAPIError:
        raise
    except Exception as e:
        # Raise a custom exception.
        raise SixtyDBAPIError from e
