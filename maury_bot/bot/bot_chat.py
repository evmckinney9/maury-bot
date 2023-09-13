from datetime import timedelta

import asyncio
import aiohttp

async def fetch_channel_history(channel, limit=None, after=None, retries=3, delay=5):
    for i in range(retries):
        try:
            if after is None:
                return [m async for m in channel.history(limit=limit)]
            else:
                return [m async for m in channel.history(limit=limit, after=after)]
        except aiohttp.client_exceptions.ClientConnectorError:
            if i < retries - 1:  # i is zero indexed
                await asyncio.sleep(delay)  # Wait for some time before trying again
                continue
            else:
                raise  # Re-raise the exception if all retries fail

async def construct_chat_history(bot, channel, reaction=None, mentions=None):
    """
    Builds chat history to pass as context to the model
    Optionally, which acts like a stopping point (look from current to past up to reacted message)
    Rules for history, max N messages, -60 seconds, stop if hit a message in responded_to cache
    Example API json arg: "messages": [{"role": "user", "content": "Hello!"}]
    """
    N = 10
    # First, get the last N messages
    if reaction is None:
        message_list = await fetch_channel_history(channel, limit=N)
    else:
        # get messages before the reacted message, +1 second to include the reacted message itself
        message_list = await fetch_channel_history(channel, limit=N, after=reaction.message.created_at)

    # Next, sort by time 
    message_list = sorted(message_list, key=lambda m: m.created_at, reverse=True)

    # if a message is '/clear', then don't look at messages earlier than that
    if any([m.content == '/clear' for m in message_list]):
        message_list = message_list[:message_list.index(next(m for m in message_list if m.content == '/clear'))]

    # reverse again to get back to chronological order
    message_list = sorted(message_list, key=lambda m: m.created_at, reverse=False)

    # turn into a list of dicts, "role" is either "user", or "assistant"
    # message_json = [{"role": m.author.display_name, "content": m.content} for m in message_list]
    # if bot is the author, then role is "assistant"
    # prepend discord display name to all messages from bot and user
    # message_json = [{"role": "assistant" if m.author == bot.user else "user", "content": m.author.display_name + ": " + m.content} for m in message_list]
    message_json = []
    for m in message_list:
        if m.author == bot.user:
            message_json.append({"role": "assistant", "content": m.content})
        else:
            message_json.append({"role": "user", "content": m.author.display_name + ": " + m.content})
    

    # DEPRECATE, in GPT3.5+, should be able to identify itself in context
    # # Then, if there exists a message in the cache, remove all messages before it
    # # this is to separate context of a message from any other that has already been responded to'
    # if any([m.id in bot.responded_to_messages for m in message_list]):
    #     #TODO test this
    #     message_list = message_list[message_list.index(next(m for m in message_list if m.id in bot.responded_to_messages)):]
    
    # # NOTE, messages from the bot itself should also count as stopping points
    # if any([m.author == bot.user for m in message_list]):
    #     message_list = message_list[message_list.index(next(m for m in message_list if m.author == bot.user)):]
    
    # finally all mentions need to be passed along for string building later
    if mentions is None:
        mentions = [] # initialize if not passed in
    mentions.extend([mention for message in message_list for mention in message.mentions]) #XXX unreadable garbage
    mentions = list(set(mentions)) # remove duplicates
    return message_json, mentions

import yaml

def get_emote_response(emote_name, author):
    with open('maury_bot/database/emotes.yaml', 'r') as stream:
        try:
            emotes = yaml.safe_load(stream)['emotes']
        except yaml.YAMLError as e:
            print(e)
    
    for em in emotes:
        if any([emoji == emote_name for emoji in em['emojis']]):
            return em['prompt'].format(author=author)
    
    return None
