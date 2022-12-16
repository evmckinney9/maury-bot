import os
import openai
import json
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import numpy as np
from helpers import checks
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
        embed = discord.Embed(
            title="I got a movie for ya jackass,",
            description="Beverely Hills Chihuahua 2 (ó﹏ò｡) ",
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

    @commands.hybrid_command(
        name="chat",
        description="Hey Maury, how are you doing today?",
    )
    
    @checks.not_blacklisted()
    async def chat(self, context: Context) -> None:
        """
        :param context: The hybrid command context.
        """
        title_list  = [
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
        embed = discord.Embed(
            title=np.random.choice(title_list),
            description=chatgpt3("A quick silly concerning greeting from a desolate old sea faren captain at a wharf"),
            color=0x3256a8
        )
        await context.send(embed=embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Maury(bot))



def chatgpt3(prompt):
    # get api key from config.json
    with open("../config.json") as file:
        data = json.load(file)
        openai.api_key = data["openai_api_key"]

    # openai.Completion.create("This is a test", model="davinci:2020-05-03", stop=["\n", " Human:", " AI:"])

    # make a prompt
    kwargs= {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 128,
        "temperature": 1,
        "top_p": 1,
        "n": 2,
        "stream": False,
        "logprobs": None,
    }

    # generate a response
    print("Generating response...")
    # wait for a response
    response = openai.Completion.create(**kwargs)
        
    # ret the response
    print(response)
    print("Done!")
    ret = response["choices"][0]["text"]

    # strip newlines
    ret = ret.replace("\n", "")
    # remove if they exist, starting/ending qoutes
    if ret[0] == '"':
        ret = ret[1:]
    if ret[-1] == '"':
        ret = ret[:-1]
    return ret