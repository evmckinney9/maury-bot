
import os
import openai
import json
from discord.ext.commands import Context
from discord import User
import random
import re

def response_cleaner(message: str) -> str:
    """Cleans the response from GPT-3"""
    # remove newline chars
    message = message.replace("\n", "")
    message = message.replace("  ", " ")

    # don't start or end with qoutes
    if message[0] == '"':
        message = message[1:]
    if message[-1] == '"':
        message = message[:-1]

    return message


def chatgpt3(prompt: str) -> str:
    """Returns a response from GPT-3"""

    # get api key from config.json
    with open("config.json") as file:
        data = json.load(file)
        openai.api_key = data["openai_api_key"]

    # make a prompt
    kwargs= {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 128,
        "temperature": 1,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "logprobs": None,
    }

    # generate a response
    print("Generating response...")
    response = openai.Completion.create(**kwargs)
    print(response)
    ret = response["choices"][0]["text"]
    ret = response_cleaner(ret)
    return ret

async def bot_response(context: Context, prompt: str, author: User=None, reactor: User=None, mentions: list[User]=None):
    """Create and respond to the prompt with a message to the channel"""
    async with context.typing():
        #personality
        prompt += "Respond with the personality of a quirky, jaded, desolate, salty seafaring captain named Maury at a fisherman's wharf.\n"

        # small chance he knows his own name
        if random.random() > 0.1:
            prompt = prompt.replace("named Maury ", "")
        
        if author is not None:
            prompt += f"Remember that {author.display_name} wrote this message.\n"
        if reactor is not None and reactor != author:
            prompt += f"Remember that {reactor.display_name} reacted to the message.\n"

        # parsed for tagged user in the original message part of the prompt
        if mentions is not None:
            for user in mentions:
                prompt = prompt.replace(f"<@{user.id}>", user.display_name)

        print(prompt)
        response_text = chatgpt3(prompt)
    
        #sub tags in response if author or reactors kwargs
        # clean response_text, want to replace names with discord mentions
        # remove @
        response_text = response_text.replace("@", "")
        if author is not None:
            # response_text = response_text.replace(author.display_name, author.mention)
            # replace all instances, case insensitive
            response_text = re.sub(author.display_name, author.mention, response_text, flags=re.IGNORECASE)
        if reactor is not None:
            # response_text = response_text.replace(reactor.display_name, reactor.mention)
            response_text = re.sub(reactor.display_name, reactor.mention, response_text, flags=re.IGNORECASE)
        
        await context.send(response_text)
