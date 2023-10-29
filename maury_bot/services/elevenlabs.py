from elevenlabs import voices, generate
from elevenlabs import set_api_key
from elevenlabs.api import VoiceSettings
from discord import FFmpegPCMAudio
import io

from elevenlabs import voices, generate
from elevenlabs import set_api_key
from elevenlabs.api import VoiceSettings
from discord import FFmpegPCMAudio
import io


async def get_elevenlabs_audio(bot, message: str):
    bot.logger.info("Generating audio stream...")

    try:
        set_api_key(bot.config["elevenlabs_api_key"])

        # get voice ID, or a random voice if none (or on failure)
        voice_list = voices()
        voice = next((v for v in voice_list if v.name == bot.NAME), None)
        if not voice:
            voice = voice_list[0]

        # configure voice settings
        voice.settings = VoiceSettings(
            stability=0.3,
            similarity_boost=0.85,
            style=0.5,
            use_speaker_boost=False,
        )
        audio_stream = generate(
            text=message,
            voice=voice,
            # model="eleven_multilingual_v2",
            model="eleven_monolingual_v1",
            stream=True,
        )
        audio = b""
        for chunk in audio_stream:
            if chunk is not None:
                audio += chunk

        # Convert bytes to AudioSource using FFmpegPCMAudio
        audio_source = FFmpegPCMAudio(
            executable="ffmpeg", source=io.BytesIO(audio), pipe=True
        )

        return audio_source

    except Exception as e:
        bot.logger.error(f"Error generating audio from ElevenLabs: {e}")
        # Handle the error in an appropriate way for your bot, such as sending an error message to the user.
        # Here, I'm raising the error again to let the calling function handle it. Adjust as necessary.
        raise
