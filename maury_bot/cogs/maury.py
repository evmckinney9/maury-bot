import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import numpy as np
from helpers import checks
from maury_bot.chatgpt3 import chatgpt3
""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


# Here we name the cog and create a new class for the cog.
class Maury(commands.Cog, name="maury"):
    def __init__(self, bot):
        self.bot = bot
        self.title_list = [
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

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    
    @commands.hybrid_command(
        name="movie",
        description="Hey Maury, what movie should I watch?",
    )
    @checks.not_blacklisted()
    async def movie(self, context: Context) -> None:
        """
        :param context: The hybrid command context.
        """
        # embed = discord.Embed(
        #     title="I got a movie for ya jackass,",
        #     description="Beverely Hills Chihuahua 2 (ó﹏ò｡) ",
        #     color=0xE02B2B
        # )
        # await context.send(embed=embed)
        await context.defer()  # This will defer the response, so the user will see a loading state
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get("https://script.google.com/macros/s/AKfycbygn4fG-jiZqmIrqmiSDyzy8cOjeXDHUPAhA5OHVqLPW0WQLhn172dU3b-K5T2eg8pVPw/exec") as request:
                if request.status == 200:
                    data = await request.json()
                    movie_str = data["movie"]
                    embed = discord.Embed(
                        title=np.random.choice(self.title_list),
                        description=chatgpt3(f"Drunkedly recommend the movie {movie_str} as a desolate salty sea captain at a fisherman's wharf"),
                        color=0x9C84EF
                    )
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
        requester = f"@{context.author.display_name}"
        embed = discord.Embed(
            title=np.random.choice(self.title_list),
            description=chatgpt3(f"A quick silly yet foreboding greeting to {requester} from a desolate old sea faren captain at a wharf"),
            color=0x3256a8
        )
        await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Maury(bot))