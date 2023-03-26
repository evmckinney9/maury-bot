
from __future__ import annotations
import openai
import json
from discord.ext.commands import Context
from discord import User
import random
import re

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from maury_bot.bot.variableBot import Persona

class PersonalityHandler():
    def __init__(self, persona: Persona):
        self.personality = persona.get_personality()
        self.name = persona.get_name()
    
    async def respond(self, context:Context, message_list:List[str], voice_message=False, **kwargs) -> str:
        """Returns a response from GPT-3
        params:
            voice_message: bool, if true, changes to a `translate` prompt and returns text as string instead of sending to channel
            (set to false to immediately send the response to the channel)
        """
        if not voice_message:
            messager = self.MessageHandler(self, context, message_list, **kwargs)
            response_text = await messager.bot_response()
            await context.send(response_text)
        else:
            messager = self.MessageHandler(self, 0, message_list, **kwargs)
            response_text = await messager.bot_response()
        return response_text
    
    class MessageHandler():
        def __init__(self, personaHandler: PersonalityHandler, context:Context, message_list:List[str], **kwargs):
            self.personality = personaHandler.personality
            self.name = personaHandler.name
            self.context = context
            self.message_list = message_list
            if self.context is None:
                raise ValueError("missing context")
            if self.message_list is None:
                # give warning, might gpt might not go first
                # NOTE needs debug, if this case breaks, just give message_list 
                # something default, like "hello" from user (?)
                print("WARNING: message_list is None")

            self.prompt = kwargs.get("prompt", None)
            self.author: User = kwargs.get("author", None)
            self.reactor: User = kwargs.get("reactor", None)
            self.mentions = kwargs.get("mentions", None)

        async def bot_response(self):
            """Create and respond to the prompt with a message to the channel"""
            if self.context != 0: # 0 indicates voice message, mean's we don't want to wrap in async typing
                async with self.context.typing():
                    self.prompt_cleaner(self.prompt)
                    print(self.prompt)
                    ret = self.chatgpt()
                    response_text = self.response_cleaner(ret)
                    return response_text

            else: # if context == 0, don't wrap in async typing
                # XXX assuming this case is only true for voice messages
                assert self.context == 0
                prompt = self.prompt_cleaner(self.prompt, reprhase=True)
                print(prompt)
                ret = self.chatgpt(prompt)
                response_text = self.response_cleaner(ret)
                return response_text

        def prompt_cleaner(self, prompt: str, reprhase=False) -> str:
            if not reprhase:
                #personality
                prompt += f"Write your discord message response using personality of: {self.personality}\n"
            else:
                prompt += f"Rephrase this message into the voice of: {self.personality}\n"

            # small chance they knows their own name
            if random.random() > 0.1:
                prompt = prompt.replace(f"named {self.name} ", "")
            
            # larger chance to mention current location 
            # TODO keep this?, helps with variability
            if random.random() > 0.15:
                # prompt = prompt.replace(f"at a {self.personality.location} ", "")
                # use regular expression to remove location, multi-word until next new line
                prompt = re.sub(r"at a [a-zA-Z ]+\n", ".\n", prompt)
            
            if self.reactor is not None and self.reactor != self.author:
                # prompt += f"Remember that {self.reactor.display_name} reacted to the message and mention them.\n"
                prompt += f"You and {self.reactor.display_name} have the same reaction to the message.\n"

            if self.author is not None:
                # prompt += f"Remember that {self.author.display_name} wrote this message and mention them.\n"
                prompt += f"{self.author.display_name} wrote the message you are responding to. Be sure to tag them.\n"

            # remove emotes, use re <:emote:1234567890> and replace with emote name
            prompt = re.sub(r"<:([^:]+):[0-9]+>", r"\1", prompt)

            # parsed for tagged user in the original message part of the prompt
            if self.mentions is not None:
                for user in self.mentions:
                    prompt = prompt.replace(f"<@{user.id}>", user.display_name)
            
            self.prompt = prompt

        def response_cleaner(self, message: str) -> str:
            """Cleans the response from GPT-3"""
            # remove newline chars
            message = message.replace("\n", "")
            message = message.replace("  ", " ")

            # don't start or end with qoutes
            if message[0] == '"':
                message = message[1:]
            if message[-1] == '"':
                message = message[:-1]

            #sub tags in response if author or reactors kwargs
            # clean response_text, want to replace names with discord mentions
            # remove @
            message = message.replace("@", "")
            if self.author is not None:
                # response_text = response_text.replace(author.display_name, author.mention)
                # replace all instances, case insensitive
                message = re.sub(self.author.display_name, self.author.mention, message, flags=re.IGNORECASE)
            if self.reactor is not None:
                # response_text = response_text.replace(reactor.display_name, reactor.mention)
                message = re.sub(self.reactor.display_name, self.reactor.mention, message, flags=re.IGNORECASE)

            return message

        def chatgpt(self) -> str:
            """Returns a response from GPT-3"""

            # get api key from config.json
            with open("config.json") as file:
                data = json.load(file)
                openai.api_key = data["openai_api_key"]

            # make a prompt
            kwargs= {
                "model": "gpt-3.5-turbo",
                "prompt": self.prompt,
                "messages": self.message_list,
                "max_tokens": 140,
                "temperature": 1,
                "top_p": 1,
                "n": 1,
                "stream": False,
                "logprobs": None,
                "presence_penalty": .25,
                "frequency_penalty": .25,
            }

            # generate a response
            print("Generating response...")
            response = openai.Completion.create(**kwargs)
            print(response)
            ret = response["choices"][0]["text"]
            return ret
