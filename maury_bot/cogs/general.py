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
from maury_bot.helpers.elevenlabs import get_voice_message
from threading import Thread, Lock

class General(commands.Cog, name="general"):
    """
    List of commands:
        - Help
        - Ping
        - Speak
        - Repeat
        - not crazy ;)
    """
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
            # if message_arg in qoutes, then use that exactly as the message
            # otherwise, use the message as a prompt to the bot
            if message_arg[0] == '"' and message_arg[-1] == '"':
                bot_message = message_arg[1:-1]
            else:
                # convert message to personality
                # NOTE context should not matter here, since gets overridden when send_it is False
                # ({"role": "user", "content": m.author.display_name + ": " + m.content}
                message_list = [{"role": "user", "content": message_arg}]
                bot_message = await self.bot.get_response(context=channel, message_list= message_list, voice_message=True)
            self.bot.voice_message = bot_message

            # ret = get_voice_message("Captain Maury", "Hey Kid,... scram!")
            status, fp = get_voice_message(self.bot.get_name(), bot_message)
            self.bot.voice_file_path = fp

            if status == 0:
                # failed, send message
                await context.send(fp, ephemeral=True)
                # self.bot.voice_message_mutex.release() # don't use, will still execute finally
                return
                # NOTE, optionally could set fp to default instead
                # fp = "maury_bot/database/synthesized_audio/default_audio.mp3"

            # join vc, play mp3, disconnect
            vc = await channel.connect()
            # await asyncio.sleep(.5) # wait to connect
            # def disconnect(error):
            #     asyncio.run_coroutine_threadsafe(vc.disconnect(), self.bot.loop)
            vc.play(discord.FFmpegPCMAudio(fp)) #, after=disconnect)

            # Wait for the audio file to finish playing
            while vc.is_playing():
                await asyncio.sleep(1)
            await asyncio.sleep(1) # wait to disconnect?
            
            await vc.disconnect()

            # Send the message after the audio file has finished playing
            await context.send(self.bot.voice_message, ephemeral=False)

        finally:
            self.bot.voice_message_mutex.release()
       
    @commands.hybrid_command(
        name="repeat",
        description="Bot joins call, repeats last thing it said"
    )
    @checks.not_blacklisted()
    async def repeat(self, context: Context) -> None:
        galley_channel_id = 818370274126069828
        channel = self.bot.get_channel(galley_channel_id)
        await context.defer(ephemeral=False)

        fp = "maury_bot/database/synthesized_audio/audio.mp3"

        try:
            message = self.bot.voice_message
        except:
            message = "Clean your ears, boy."
    
        vc = await channel.connect()
        # await asyncio.sleep(.5) # wait to connect
        # def disconnect(error):
        #     asyncio.run_coroutine_threadsafe(vc.disconnect(), self.bot.loop)
        vc.play(discord.FFmpegPCMAudio(fp)) #, after=disconnect)

        # Wait for the audio file to finish playing
        while vc.is_playing():
            await asyncio.sleep(1)
        await asyncio.sleep(1) # wait to disconnect?
        await vc.disconnect()

        # Send the message after the audio file has finished playing
        await context.send(message, ephemeral=False)

    @commands.hybrid_command(
        name="not_crazy",
        description="blah",
    )
    @checks.not_blacklisted()
    async def not_crazy(self, context: Context) -> None:
        # join VC and play the default audio
        galley_channel_id = 818370274126069828
        channel = self.bot.get_channel(galley_channel_id)
        await context.defer(ephemeral=False)
        # define some random chance
        p = 0.1
        if random.random() < p:
            # play default audio
            fp = "maury_bot/database/synthesized_audio/default_audio.mp3"
            
        else:
            # k = 3 # number of ellipses
            k = random.randint(1, 5)
            #"I uhhhh, ... am NOT crazy!"
            prompt = "I uhhhh, "
            for i in range(k):
                prompt += "... "
            prompt += "am NOT crazy!"

            # get response
            # ret = get_voice_message("Captain Maury", "Hey Kid,... scram!")
            status, fp = get_voice_message(self.bot.get_name(), prompt)
            self.bot.voice_file_path = fp

            if status == 0:
                # failed, send message
                await context.send(fp, ephemeral=True)
                # self.bot.voice_message_mutex.release() # don't use, will still execute finally
                return
            
        vc = await channel.connect()
        # add a delay to connect
        # await asyncio.sleep(.5)
        vc.play(discord.FFmpegPCMAudio(fp)) #, after=disconnect)

        # Wait for the audio file to finish playing
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

        # Send the message after the audio file has finished playing
        await context.send("I'm not crazy, you're crazy!", ephemeral=False)

async def setup(bot):
    await bot.add_cog(General(bot))
