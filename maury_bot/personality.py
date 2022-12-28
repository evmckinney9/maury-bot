# create abstract class for personalities
from abc import ABC
from maury_bot.chatgpt3 import PersonalityHandler
import random
from discord.ext.commands import Bot, Context
from discord import Intents
import discord
from functools import partial

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents
"""

class AbstractBotPersonality(ABC):
    def __init__(self) -> None:
        return
        # TODO these are the abstract attributes
        # self.name = None
        # self.adjectives = None
        # self.occupation = None
        # self.location = None
        # self.statuses = None
    
    def get_name(self) -> str:
        return self.name

    def get_personality(self) -> str:
        return f"a {', '.join(self.adjectives)} {self.occupation} at a {self.location}"
    
    def get_handler(self) -> PersonalityHandler:
        return self.handler

class AbstractBot(ABC, Bot):
    """persona interface"""
    def __init__(self):
        # TODO these are the abstract attributes
        # self.handler = None
        Bot.__init__(self, command_prefix="/", intents=Intents.all(), help_command=None)
        
    # def get_name(self) -> str:
    #     return self.name
    
    def get_response(self, context: Context, prompt:str, **kwargs)-> str:
        """Returns a response from GPT-3
        Optional kwargs:
        author: User
        reactor: User
        mentions: list of Users
        """
        handler = self.get_handler()
        return handler.respond(context, prompt, **kwargs)
    
    # def get_personality(self) -> str:
    #     raise NotImplementedError

    def get_status(self) -> str:
        return random.choice(self.statuses)

# NOTE order matters here
# multiple inheritance points get_personality to the Persona class
class MauryBot(AbstractBotPersonality, AbstractBot):
    def __init__(self):
        AbstractBotPersonality.__init__(self)
        self.name = "Captain Maury"
        self.adjectives = ["drunkard", "jaded", "desolate", "grungy", "salty", "seafaring"]
        self.occupation = "ghost captain"
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
        AbstractBot.__init__(self)
        self.handler = PersonalityHandler(self)
        self.avatar_file = "maury_bot/avatars/maury.png"
        # load file into bytes
        with open(self.avatar_file, "rb") as f:
            self.avatar = f.read()

class DottyBot(AbstractBotPersonality, AbstractBot):
    def __init__(self):
        AbstractBotPersonality.__init__(self)
        self.name = "Dotty Spaghettini"
        self.adjectives = ["cranky", "sarcastic", "distracted", "cynical", "disillusioned", "gambling woman"]
        self.occupation = "mob boss divorcée"
        self.location = "smoking section of dim casino, rusty slot machines"
        self.statuses = [
                "the clatter of dice",
                "the clink of glasses"
            ]
        AbstractBot.__init__(self)
        self.handler = PersonalityHandler(self)
        self.avatar_file = "maury_bot/avatars/dotty.png"
        # load file into bytes
        with open(self.avatar_file, "rb") as f:
            self.avatar = f.read()

class VariablePersonaBot(AbstractBot):
    def __init__(self, persona: AbstractBotPersonality = MauryBot()):
        self.current_bot = None
        self.get_name = None
        self.get_personality = None
        self.get_status = None
        self.get_handler = None
        self.avatar = None
        self.switch_to(persona)
        self.responded_to_messages = []
        self.high_activity = 0
        super().__init__()

    def switch_to(self, bot: AbstractBotPersonality=None):
        """Switches the current bot to the given bot"""
        if bot is None and isinstance(self.current_bot, MauryBot):
            bot = DottyBot()
        elif bot is None and isinstance(self.current_bot, DottyBot):
            bot = MauryBot()

        self.current_bot = bot
        self.get_name = partial(self.current_bot.get_name)
        self.get_personality = partial(self.current_bot.get_personality)
        self.get_status = partial(self.current_bot.get_status)
        self.get_handler = partial(self.current_bot.get_handler)
        self.avatar = self.current_bot.avatar

    #XXX careful, rate limiting prevents this from being called, only once every 10 minutes (?)
    async def discord_refresh_persona(self):
        """Updates the bot's name, avatar, flair, description, and status"""
        # switch bot nickname
        await self.user.edit(username=self.get_name())
        # switch bot avatar
        await self.user.edit(avatar=self.avatar)
        # switch bot status
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=self.get_status()))
