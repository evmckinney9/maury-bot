import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import numpy as np
from helpers import checks
from maury_bot.chatgpt3 import bot_response
""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

title_list = [
        "*Gulp*",
        "*Cough*",
        "*Grunt*",
        "*Hyeem*",
        "*Heem*",
        "*Ahem*",
        "*Hmm*",
        "*Hobble*",
        "*Wheeze*",
        "*Sigh*",
]

# Here we name the cog and create a new class for the cog.
class Maury(commands.Cog, name="maury"):
    def __init__(self, bot):
        self.bot = bot
        self.title_list = title_list

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_command(
        name="movie",
        description="Hey Maury, what movie should I watch?",
    )
    @checks.not_blacklisted()
    async def movie(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://script.google.com/macros/s/AKfycbygn4fG-jiZqmIrqmiSDyzy8cOjeXDHUPAhA5OHVqLPW0WQLhn172dU3b-K5T2eg8pVPw/exec") as request:
                if request.status == 200:
                    spreadsheet_data = await request.json()
                    movie_str = spreadsheet_data["movie"]
                    await bot_response(context=context, prompt=f"Drunkedly recommend the movie {movie_str}")
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)

    @commands.hybrid_command(
        name="chat",
        description="Hey Maury, how are you doing today?",
    )
    
    @checks.not_blacklisted()
    async def chat(self, context: Context) -> None:
        """
        :param context: The hybrid command context.
        """
        # get requester
        # await context.defer()
        async with context.typing():
            author = f"{context.author.display_name}"
            await bot_response(context=context, prompt=f"Make a quick, silly yet foreboding greeting to {author}", author=context.author)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Maury(bot))