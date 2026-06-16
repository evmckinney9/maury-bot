"""Provider-agnostic text-to-speech dispatcher.

Selects the TTS backend based on the ``tts_provider`` field in config.json
("60db" by default, or "elevenlabs"). Both backends share the same
``get_*_audio(bot, message)`` signature and return a discord AudioSource, so
voice command playback stays identical regardless of provider.
"""

from maury_bot.services.elevenlabs import ElevenLabsAPIError, get_elevenlabs_audio
from maury_bot.services.sixtydb import SixtyDBAPIError, get_sixtydb_audio


class TTSError(Exception):
    """Provider-agnostic text-to-speech error."""

    pass


async def get_tts_audio(bot, message: str):
    """Generate speech audio using the configured TTS provider."""
    provider = bot.config.get("tts_provider", "60db").lower()

    try:
        if provider == "elevenlabs":
            return await get_elevenlabs_audio(bot, message)
        # Default to 60db for any other value (including "60db"/"sixtydb").
        return await get_sixtydb_audio(bot, message)
    except (ElevenLabsAPIError, SixtyDBAPIError) as e:
        bot.logger.error(f"TTS provider '{provider}' failed: {repr(e)}")
        raise TTSError from e
