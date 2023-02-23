""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

import asyncio
import os
import platform
import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context
import numpy as np
from helpers import checks
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from maury_bot.bot import AbstractBot
from elevenlabs import get_voice_message
from threading import Thread, Lock

class General(commands.Cog, name="general"):
    def __init__(self, bot: "AbstractBot"):
        self.bot = bot
        self.bot.voice_message_mutex = Lock()

    @commands.hybrid_command(
        name="help",
        description="List all commands the bot has loaded."
    )
    @checks.not_blacklisted()
    async def help(self, context: Context) -> None:
        embed = discord.Embed(
            title="Hey Kid,", description="scram", color=0x9C84EF)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        context.bot.tree.copy_global_to(guild=context.guild)
        await context.bot.tree.sync(guild=context.guild)
        embed = discord.Embed(
            title="Hey kid,",
            description=f"scram!",
            color=0x9C84EF
        )
        await context.send(embed=embed)
    
    @commands.hybrid_command(
        name="repeat",
        description="Bot joins call, repeats last thing it said"
    )
    @checks.not_blacklisted()
    async def repeat(self, context: Context) -> None:
        try:
            galley_channel_id = 818370274126069828
            channel = self.bot.get_channel(galley_channel_id)
            context.defer(ephemeral=False)
            # join vc, play mp3, disconnect
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(self.bot.voice_file_path)) #, after=lambda e: print('done', e))
            while vc.is_playing():
                await asyncio.sleep(1)
            await vc.disconnect()

            # reply back to channel with what was spoken
            await context.send(self.bot.voice_message, ephemeral=False) 
        except:
            await context.send("I haven't said anything yet!", ephemeral=True)

    @commands.hybrid_command(
        name="speak",
        description="Bot joins call, drops a knowledge bomb"
    )
    @checks.not_blacklisted()
    async def speak(self, context: Context, message_arg: str) -> None:
        """
        Bot joins call, drops a knowledge bomb

        :param context: The hybrid command context.
        """
        galley_channel_id = 818370274126069828
        channel = self.bot.get_channel(galley_channel_id)
        # defer
        await context.defer(ephemeral=False)

        # here need to wait until bot frees up the voice_message mutex
        self.bot.voice_message_mutex.acquire()
        
        try:
            # convert message to personality
            # NOTE context should not matter here, since gets overridden when send_it is False
            bot_message = await self.bot.get_response(context=channel, prompt= message_arg+'\n', voice_message=True)
            self.bot.voice_message = bot_message

            # ret = get_voice_message("Captain Maury", "Hey Kid,... scram!")
            status, fp = get_voice_message(self.bot.get_name(), bot_message)
            self.bot.voice_file_path = fp

            if status == 0:
                # failed, send message
                await context.send(fp, ephemeral=True)
                self.bot.voice_message_mutex.release()
                return
                # NOTE, optionally could set fp to default instead
                # fp = "maury_bot/database/synthesized_audio/default_audio.mp3"

            # join vc, play mp3, disconnect
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(fp)) #, after=lambda e: print('done', e))
            while vc.is_playing():
                await asyncio.sleep(1)
            await vc.disconnect()

            # reply back to channel with what was spoken
            await context.send(bot_message, ephemeral=False) 

        finally:
            self.bot.voice_message_mutex.release()

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(
        name="movie",
        # description=f"Hey {self.bot.name}, What movie should I watch?",
        description="What movie should I watch?",
    )
    @checks.not_blacklisted()
    async def movie(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://script.google.com/macros/s/AKfycbygn4fG-jiZqmIrqmiSDyzy8cOjeXDHUPAhA5OHVqLPW0WQLhn172dU3b-K5T2eg8pVPw/exec") as request:
                if request.status == 200:
                    spreadsheet_data = await request.json()
                    movie_str = spreadsheet_data["movie"]
                    await self.bot.get_response(context=context, prompt=f"Response: a recommendation for the movie {movie_str}.\n")
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
