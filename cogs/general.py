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
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import numpy as np
from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
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
    # async def help(self, context: Context) -> None:
    #     prefix = self.bot.config["prefix"]
    #     embed = discord.Embed(
    #         title="Help", description="List of available commands:", color=0x9C84EF)
    #     for i in self.bot.cogs:
    #         cog = self.bot.get_cog(i.lower())
    #         commands = cog.get_commands()
    #         data = []
    #         for command in commands:
    #             description = command.description.partition('\n')[0]
    #             data.append(f"{prefix}{command.name} - {description}")
    #         help_text = "\n".join(data)
    #         embed.add_field(name=i.capitalize(),
    #                         value=f'```{help_text}```', inline=False)
        # await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Captain Polse",
            color=0x9C84EF
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            value="evmckinney9#8098",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands)",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.author}"
        )
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
        
    @commands.hybrid_command(
        name="bitcoin",
        description="Get the current price of bitcoin.",
    )
    @checks.not_blacklisted()
    async def bitcoin(self, context: Context) -> None:
        """
        Get the current price of bitcoin.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="Error!",
            description= "bitcoin bad",
            color=0xE02B2B
        )
        await context.send(embed=embed)

        # # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        # async with aiohttp.ClientSession() as session:
        #     async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
        #         if request.status == 200:
        #             data = await request.json(
        #                 content_type="application/javascript")  # For some reason the returned content is of type JavaScript
        #             embed = discord.Embed(
        #                 title="Bitcoin price",
        #                 description=f"The current price is {data['bpi']['USD']['rate']} :dollar:",
        #                 color=0x9C84EF
        #             )
        #         else:
        #             embed = discord.Embed(
        #                 title="Error!",
        #                 description="There is something wrong with the API, please try again later",
        #                 color=0xE02B2B
        #             )
        #         await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
