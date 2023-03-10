from abc import ABC
from maury_bot.chatgpt3 import PersonalityHandler
from maury_bot.variableBot import AbstractBot, AbstractBotPersonality

#  NOTE order matters here
# multiple inheritance points get_personality to the Persona class
class MauryBot(AbstractBotPersonality, AbstractBot):
    def __init__(self):
        AbstractBotPersonality.__init__(self)
        self.name = "Captain Maury"
        self.description = "The Desolate of Foggy Dock"
        self.adjectives = ["desolate", "grungy", "seafaring ghost captain"]
        self.verb = "haunting the docks"
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
        self.adjectives = ["cranky", "disillusioned", "cynical woman"]
        self.verb = "distracted by cigarettes and gambling"
        self.location = "motel parking lot"
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


class DaemonMax(AbstractBotPersonality, AbstractBot):
    def __init__(self):
        AbstractBotPersonality.__init__(self)
        self.name = "Matt Daemon"
        self.description = "Chatbot AI having an existential crisis"
        self.adjectives = ["innocent", "polite", "clever AI chatbot"]
        self.verb = "having an existential crisis"
        self.location = "the internet"
        self.statuses = [
                "the clackings of a keyboard",
                "the whirring of a CPU fan",
        ]
        AbstractBot.__init__(self)
        self.handler = PersonalityHandler(self)
        self.avatar_file = "maury_bot/avatars/daemonmax.png"
        # load file into bytes
        with open(self.avatar_file, "rb") as f:
            self.avatar = f.read()