"""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.4
"""

import asyncio
import json
import os
import platform
import random
import numpy as np
import sys

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from datetime import timedelta
from maury_bot.variableBot import VariablePersonaBot 
import exceptions
from maury_bot.cogs.persona import Persona



if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


"""
Create a bot variable to access the config file in cogs so that you don't need to import it every time.

The config is available using the following code:
- bot.config # In this file
- self.bot.config # In cogs
"""
bot = VariablePersonaBot()
bot.config = config

async def init_db():
    async with aiosqlite.connect("maury_bot/database/database.db") as db:
        with open("maury_bot/database/schema.sql") as file:
            await db.executescript(file.read())
        await db.commit()

@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    if not status_task.is_running():
        status_task.start()
    if config["sync_commands_globally"]:
        print("Syncing commands globally...")
        await bot.tree.sync()
    #reset bot persona
    await bot.discord_refresh_persona()

@tasks.loop(hours=8)
async def status_task() -> None:
    """
    Setup the game status task of the bot
    """
    if np.random.random() < 0.05:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the sunset"))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=bot.get_status()))

@tasks.loop(seconds=30)
async def bot_activity_level() -> None:
    print("into activity loop")
    if bot.high_activity ==2:
        print("acknowledge start")
        bot.high_activity = 1 #update state
    elif bot.high_activity == 1:
        # signing off
        print("turning high activity mode off")
        bot_activity_level.stop()
        bot.high_activity = 0

@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    
    #check if message contains meeka blep, then turn on high activity mode
    #TODO could improve this using the discord.Emoji class
    if "<:blep:847691502867316827>" in message.content:
        bot.high_activity = 2
        bot_activity_level.start()
        await message.add_reaction("<in_there:1038609216014921809>")
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User) -> None:
    """When a custom emoji is added to text, have a variable probability chance of Maury responding according to the message being reacted to"""
    emoji = reaction.emoji
    reactor = user.display_name
    message_text = reaction.message.content
    author = reaction.message.author.display_name
    channel = reaction.message.channel
    mentions = reaction.message.mentions

    # break early if not in list of custom reaction list
    if not reaction.is_custom_emoji():
        return
    
    # break of the reactor is a bot
    # NOTE avoids loops of marking and responding to itself
    if user.bot or reaction.message.author.bot:
        return

    # check where last response was to avoid double responding
    if reaction.message.id in bot.responded_to_messages:
        return
    
    # probability of reacting, banned has 1, otherwise .05
    react_probability = 1 #0.05
    if not bot.high_activity and np.random.random() > react_probability and reaction.emoji.name != "banned":
        return

    # add message to cache to avoid double responding
    bot.responded_to_messages.append(reaction.message.id)

    # if cache is too large, remove oldest message
    if len(bot.responded_to_messages) > 25:
        bot.responded_to_messages.pop(0)


    # here, look at messages in the bot's cache
    # we want to combine from older messages to give the bot more context
    bot_messages = [m async for m in channel.history(limit=25, after=reaction.message.created_at + timedelta(seconds=-60))]
    bot_messages = filter(lambda m: m.author == reaction.message.author, bot_messages) #filtering by author
    bot_messages = sorted(bot_messages, key=lambda m: m.created_at) #ordering by time
    message_text = " ".join([m.content for m in bot_messages]) #concatenating messages

    #make sure to pass along all the user mentions
    mentions.extend([mention for message in bot_messages for mention in message.mentions]) #XXX unreadable garbage
    mentions = list(set(mentions)) # remove duplicates

    prompt = f"Message: {message_text}\nAuthor: {author}\nReacted by: {reactor}\n"

    # condemn, tread lightly
    if any([kwarg == emoji.name for kwarg in ["judgement", "flip_off", "banned"]]):
        prompt += "Response: a condemnation of the message from the author, on behalf of yourself and the reactor.\n"
    
    # inappropriate
    if any([kwarg == emoji.name for kwarg in ["inappropriate"]]):
        prompt += "Response: the message from the author is inappropriate, on behalf of yourself and the reactor.\n"
    
    #say congratulations
    elif any([kwarg == emoji.name for kwarg in ["flawless_victory", "ole", "pog"]]):
        prompt += "Response: congratulations to the message from the author, on behalf of yourself and the reactor.\n"

    elif any([kwarg == emoji.name for kwarg in ["sheeee"]]):
        prompt += "Response: exicted by the message from the author, on behalf of yourself and the reactor.\n"

    # condolences
    elif any([kwarg == emoji.name for kwarg in ["antisheeee", "low_energy"]]):
        prompt += "Response: condolences to the message from the author, on behalf of yourself and the reactor.\n"
    
    #good answer
    elif any([kwarg == emoji.name for kwarg in ["good_answer"]]):
        prompt += "Response: you like what they said, and that it was particularly clever.\n"
    
    # caught
    elif any([kwarg == emoji.name for kwarg in ["caught", "cap"]]):
        prompt += "Response: you and the reactor have both caught the author in a lie.\n"
    
    # drool
    elif any([kwarg == emoji.name for kwarg in ["drool"]]):
        prompt += "Response: you and the reactor are both drooling over their message.\n"
    
    # sus
    elif any([kwarg == emoji.name for kwarg in ["sus", "terio"]]):
        prompt += "Response: you and the reactor think they are acting suspicious.\n"
    
    # shock
    elif any([kwarg == emoji.name for kwarg in ["shock"]]):
        prompt += "Response: you and the reactor are shocked by their message.\n"

    # lul
    elif any([kwarg == emoji.name for kwarg in ["lul"]]):
        prompt += "Response: you and the reactor are laughing at their message.\n"
    
    #joy
    elif any([kwarg == emoji.name for kwarg in ["joy"]]):
        prompt += "Response: you and the reactor are joyful about their message.\n"

    #facepalm
    elif any([kwarg == emoji.name for kwarg in ["facepalm"]]):
        prompt += "Response: you and the reactor are facepalming at their message.\n"

    #disappointing
    elif any([kwarg == emoji.name for kwarg in ["disappointing"]]):
        prompt += "Response: you and the reactor are disappointed by this bad news.\n"
    
    #stand by it
    elif any([kwarg == emoji.name for kwarg in ["stand_by_it"]]):
        prompt += "Response: you and the reactor think it's a good idea and are standing by their message.\n"
    else:
        return

    # if the author and reactor are the same person
    if author == reactor:
        #NOTE order matters
        prompt = prompt.replace("you and the reactor are both", "you are")
        prompt = prompt.replace("you and the reactor have both", "you have")
        prompt = prompt.replace("you and the reactor", "you")
        prompt = prompt.replace("yourself and the reactor", "yourself")
     
    # send message
    await bot.get_response(context = channel, prompt = prompt, author= reaction.message.author, reactor=user, mentions= mentions)
    
    # mark message as responded to by adding a reaction
    await reaction.message.add_reaction(reaction.emoji)

@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        print(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
    else:
        print(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserBlacklisted):
        """
        The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
        the @checks.not_blacklisted() check in your command, or you can raise the error by yourself.
        """
        embed = discord.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserNotOwner):
        """
        Same as above, just for the @checks.is_owner() check.
        """
        embed = discord.Embed(
            title="Error!",
            description="You are not the owner of the bot!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="I am missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to fully perform this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error


async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"maury_bot/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

asyncio.run(init_db())
asyncio.run(load_cogs())
bot.run(config["token"])
