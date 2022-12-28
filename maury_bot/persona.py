# create abstract class for personalities
from abc import ABC
from maury_bot.chatgpt3 import PersonaHandler
import random
from discord.ext.commands import Bot, Context
from discord import Intents

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents
"""

class AbstractBot(ABC, Bot):
    def __init__(self, name: str):
        self.name = name
        self.responded_to_messages = []
        self.high_activity = 0
        self.handler = PersonaHandler(self)
        super().__init__(command_prefix="/", intents=Intents.all(), help_command=None)

    def get_name(self) -> str:
        return self.name
    
    def get_response(self, context: Context, prompt:str, **kwargs)-> str:
        """Returns a response from GPT-3
        Optional kwargs:
        author: User
        reactor: User
        mentions: list of Users
        """
        return self.handler.respond(context, prompt, **kwargs)
    
    def get_personality(self) -> str:
        # list all adjectives
        return f"a {', '.join(self.adjectives)} {self.occupation} at a {self.location}"

    def get_status(self) -> list:
        return random.choice(self.statuses)

class MauryBot(AbstractBot):
    def __init__(self):
        self.adjectives = ["quirky", "jaded", "desolate", "drunk", "salty", "seafaring"]
        self.occupation = "luxury captain"
        self.location = "fisherman's wharf"
        self.statuses = [
                "the lapping of the waves against the pier",
                "the snapping of a flag in the breeze",
                "the scuffle of feet from dock workers",
                "the clang of a boat's bell",
                "the rattle of the mooring chains",
                "the chatter of fishermen",
                "the low hum of boat engines",
                "the distant rumble of thunder",
                "the gentle clinking of fishing lines",
                "the thrum of heavy cargo machinery",
            ]
        super().__init__(name="Maury")