import asyncio
from collections import deque

from discord.ext import commands
from discord.ext.commands import Context

from maury_bot.services.chatgpt import get_chatgpt_response
from maury_bot.services.elevenlabs import get_elevenlabs_audio, ElevenLabsAPIError

class Voice(commands.Cog, name="voice"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.queue = deque()
        self.lock = asyncio.Lock()

    async def play_audio(self, ctx, audio_source) -> None:
        """Joins voice channel, plays audio, and then leaves."""
        if not ctx.author.voice:
            await ctx.send("You must be in a voice channel to use this command.")
            return

        voice_client = await ctx.author.voice.channel.connect()
        voice_client.play(audio_source)

        while voice_client.is_playing():
            await asyncio.sleep(1)

        await voice_client.disconnect()

    async def handle_speak(self, ctx, audio_task):
        """Processes and plays the requested speech."""
        async with self.lock:
            audio_source = await audio_task
            await self.play_audio(ctx, audio_source)

        await self.check_queue(ctx)

    async def check_queue(self, ctx):
        """Processes the next message in the queue."""
        if self.queue:
            await self.handle_speak(ctx, self.queue.popleft())

    async def add_to_queue_or_speak(self, ctx, audio_task):
        """Determines whether to queue the message or process immediately."""
        # Check if there's any voice client playing audio
        is_voice_active = any(vc.is_playing() for vc in self.bot.voice_clients)

        if is_voice_active:
            self.queue.append(audio_task)
        else:
            await self.handle_speak(ctx, audio_task)

    @commands.hybrid_command(
        name="speak",
        description="Bot joins voice call and speaks the model response.",
    )
    async def speak(self, ctx: Context, *, message: str) -> None:
        try:
            await ctx.defer(ephemeral=False)

            message = await get_chatgpt_response(
                self.bot, [{"role": "user", "content": message}]
            )

            # replace newline characters with <break time="0.5s"/>
            message = message.replace("\n\n", '<break time="0.5s"/>')
            self.bot.logger.debug(f"Response from model: {message}")

            audio_task = asyncio.create_task(get_elevenlabs_audio(self.bot, message))
            await self.add_to_queue_or_speak(ctx, audio_task)
            await ctx.send(message)
        except ElevenLabsAPIError as e:
            self.bot.logger.error(f"Error in speak command: {e}")
            await ctx.send("Sorry, there was an error processing your request.")

    @commands.hybrid_command(
        name="recite",
        description="Bot joins voice call and recites provided text.",
    )
    async def recite(self, ctx: Context, *, message: str) -> None:
        try:
            await ctx.defer(ephemeral=False)

            audio_task = asyncio.create_task(get_elevenlabs_audio(self.bot, message))
            await self.add_to_queue_or_speak(ctx, audio_task)
            await ctx.send(message)
        except ElevenLabsAPIError as e:
            self.bot.logger.error(f"Error in recite command: {e}")
            await ctx.send("Sorry, there was an error processing your request.")

async def setup(bot) -> None:
    """Adds the Voice cog to the bot."""
    await bot.add_cog(Voice(bot))
