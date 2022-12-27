## Python Discord Bot with GPT-3 Integration

#### This discord bot will intelligently respond to you on discord, with a chance to be triggered on when users emote react to messages.

Automated content moderation reminders on your behalf, on :angry: emote
![image](https://user-images.githubusercontent.com/47376937/209484678-ec09fce5-26b3-4213-a16d-3e8f4e4d3d25.png)

Send a kind regards, on :joy: emote,
![image](https://user-images.githubusercontent.com/47376937/209484703-03a706dc-a751-4d1a-a3ca-8d4f6d2d5cdb.png)

or a sincere condolence, on :cry: emote.
![image](https://user-images.githubusercontent.com/47376937/209484689-79ec9c9b-e990-47fd-b96b-6fc10a0138c0.png)

and of course your server's custom emotes.
![image](https://user-images.githubusercontent.com/47376937/209485945-fc012e33-9eb9-4174-9bf8-5b253630b8ad.png)


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
  python -m venv maury_venv
  python -m pip install -r requirements.txt
  source maury_venv/bin/activate
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
    "openai_api_key": "YOUR_OPENAI_KEY_HERE"
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
To modify the probability that any given emote reaction triggers the bot, change `react_probability` in `bot.py`
default:
```python
react_probability = 0.05
```

To modify the bot to respond to your own custom set of emote reactions, need to edit code in `bot.py`. Future work will compartmentalize this functionality more nicely.

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
