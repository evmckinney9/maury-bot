## Python Discord Bot with GPT-3 Integration

#### I am currently working on many more features! Current README documentation is slightly outdated with [latest release](https://github.com/evmckinney9/maury-bot/releases/tag/v0.3.0)
___
#### This discord bot will intelligently respond to you on discord, with a chance to be triggered on when users emote react to messages.

Reactions on your server's custom emotes.

![image](https://user-images.githubusercontent.com/47376937/220812786-5a8883fc-efd3-4db9-a1c7-64bf2f30c772.png)

Tag @bot to respond to any message:

![image](https://user-images.githubusercontent.com/47376937/220812662-8d0e33ed-cc7f-47cb-80ae-c2c0ab96b161.png)

Responds with the server's emotes:

![image](https://user-images.githubusercontent.com/47376937/227757680-3d21122b-b850-45ef-88b5-6c242408cd86.png)


Use `/chat` to get a "Hello, World!" message.

![image](https://user-images.githubusercontent.com/47376937/210667776-d6ae0d35-06a0-4d03-a0d3-a344ed725ae9.png)

Use command `/speak` to get a voice message into the voice channel. To speak a message exactly as you type use "", otherwise will translate into the voice of your bot.

![image](https://user-images.githubusercontent.com/47376937/220812870-945ef997-53c3-4872-b546-209be9595563.png)


Trained using: https://www.youtube.com/watch?v=E-SNQo9STps

Reference: https://github.com/elevenlabs/discord-bot

```bash
sudo apt install ffmpeg
```
___
## Setup
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-396/)

Created using this template: https://github.com/kkrypt0nn/Python-Discord-Bot-Template

I use Raspberry Pi OS Lite with this application running in the background using `tmux`.

### 1. Preliminaries
  - Setup a Pi, or any other internet connected python enviroment
  - Create a discord bot https://discord.com/developers/applications
    - A suggested permissions integer: `466004442176`
    - Enable MESSAGE CONTENT INTENT
  - Obtain an Openai API key, https://beta.openai.com/account/api-keys
   
### 2. Setup repository
- Clone repo, and start python virtual enviroment
  ```shell
  git clone https://github.com/evmckinney9/maury-bot.git
  cd maury-bot
  python3.9 -m venv maury_venv
  source maury_venv/bin/activate
  python -m pip install -r requirements.txt
  pip install -e .
  touch config.json
  ```
  
- Put API keys into `config.json`
  ```json
  {
      "token": "YOUR_BOT_TOKEN_HERE",
      "permissions": "466004442176",
      "application_id": "YOUR_APPLICATION_ID_HERE",
      "sync_commands_globally": false,
      "owners": [
          "YOUR_DISCORD_USER_ID",
          502280530520440862
      ],
      "openai_api_key": "YOUR_OPENAI_KEY_HERE",
      "elevenlabs_key": "YOUR_ELEVENLABS_KEY_HERE",
  }
  ```
### 3. Start Application
  ```shell
  tmux attach
  python bot.py
  ```
  exit using `Ctrl+B, D`
  
___
## Usage

To define a bot persona, extend `AbstractBot` in `botPopulation.py` 
Example:
```python
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
```

To modify the emote triggers, edit code in `bot.py`. 
Template:
```python
# EMOTION
if any([kwarg == emoji.name for kwarg in ["emoji_name1", "emoji_name2"]):
    prompt += "Respond with EMOTION to the message from the author, on behalf of yourself and the reactor."
```

Example:
```python
# condemn, tread lightly
if any([kwarg == emoji.name for kwarg in ["judgement", "flip_off", "banned"]]):
    prompt += "Respond with a condemnation of the message from the author, on behalf of yourself and the reactor."

#say congratulations
elif any([kwarg == emoji.name for kwarg in ["sheeee", "flawless_victory", "ole", "pog"]]):
    prompt += "Respond with congratulations to the message from the author, on behalf of yourself and the reactor."
```

To modify the probability that any given emote reaction triggers the bot, change `react_probability` in `bot.py`
default:
```python
react_probability = 0.05
```

## Debugging
When debugging persona keywords/GPT queries, it is useful to have a mode that always responds so you can test the changes more rapidly. The simplest way is to change the `react_probability=1` and test in a private discord channel to avoid spamming other members. In addition, here are some other settings I find useful:
If you want to set high activity mode (react_probability=1 for 30 minutes), modify `bot.py` with your own emote ids here.
```python
@bot.event
async def on_message(message: discord.Message) -> None:
    ...
    if "<trigger:emote>" in message.content:
        bot.high_activity = 2
        bot_activity_level.start()
        await message.add_reaction("<acknowledge:emote>")
    ...
```

Also, note that I have added my "banned" emoji to always take precendence over the variable chance.
```python
# probability of reacting, banned has 1, otherwise .05
    react_probability = 1 #0.05
    if not bot.high_activity and np.random.random() > react_probability and reaction.emoji.name != "banned":
        return
```
