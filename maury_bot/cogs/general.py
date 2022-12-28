""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

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


class General(commands.Cog, name="general"):
    def __init__(self, bot: "AbstractBot"):
        self.bot = bot

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
            title="omfg",
            description=f"she ded",
            color=0x9C84EF
        )
        await context.send(embed=embed)
       
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
