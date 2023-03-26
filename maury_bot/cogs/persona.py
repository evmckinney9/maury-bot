import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import numpy as np
from helpers import checks
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from maury_bot.bot.variableBot import VariablePersonaBot

""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks

# title_list = [
#         "*Gulp*",
#         "*Cough*",
#         "*Grunt*",
#         "*Hyeem*",
#         "*Heem*",
#         "*Ahem*",
#         "*Hmm*",
#         "*Hobble*",
#         "*Wheeze*",
#         "*Sigh*",
# ]

# Here we name the cog and create a new class for the cog.
class Persona(commands.Cog, name="persona"):

    """
    Slash commands:
        - chat
        - switch
    """

    def __init__(self, bot: "VariablePersonaBot"):
        self.bot = bot
        # self.title_list = title_list

    @commands.hybrid_command(
        name="chat",
        description="How are you doing today?",
    )

    @checks.not_blacklisted()
    async def chat(self, context: Context) -> None:
        """
        :param context: The hybrid command context.
        """
        # get requester
        # await context.defer()
        author = f"{context.author.display_name}"
        # get message contents
        message = context.message.content
        # # default prompt
        # if message == f"/chat":
        #     prompt = f"A brief, silly yet foreboding greeting to {author}.\n"
        # else:
        #     prompt = f"{message}\n"
        # print(prompt)
        
        prompt = f"Give a brief, silly yet foreboding greeting to {author}.\n"
        await self.bot.get_response(context=context, prompt=prompt, author=context.author)

    @commands.hybrid_command(
        name="switch",
        description="Switch to a different persona",
    )
    @checks.not_blacklisted()
    async def switch(self, context: Context) -> None:
        self.bot.switch_to() #None param just rotates through personas
        await self.bot.discord_refresh_persona()
        # say hello
        await self.chat(context)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Persona(bot))