# # # API access to elevenlabs for voice generation

# POST
# /v1/text-to-speech/{voice_id}
# Text To Speech
# Converts text into speech using a voice of your choice and returns audio.

# voice_id *
# string
# (path)
# Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.

# xi-api-key
# string
# (header)
# Your API key. This is required by most endpoints to access our API programatically. You can view your xi-api-key using the 'Profile' tab on the website.

import requests
import json

def get_voice_message(bot_name, message_text):
    """
    params:
        bot_name: string - should match one of the voices available from elevenlabs
        message_text: string - text to be converted to speech, max 1000 characters
        For best results, pass string to persona function first
    returns:
        (status, message) - status is True if successful, False if not
        message is a string containing the filename of the audio file if successful, or an error message if not
    """

    url = "https://api.elevenlabs.io/v1/"

    if len(message_text) > 1000:
        return "Message too long, max 1000 characters"

    # get api key from config.json
    with open("config.json") as file:
        data = json.load(file)
        api_key = data["elevenlabs_key"]
        headers = {
            'accept': 'audio/mpeg',
            'xi-api-key': api_key,
            'Content-Type': 'application/json'
            }

    # first, get list of available voices
    response = requests.get(url + "voices", headers=headers)

    if response.status_code != 200:
        return (0, "Request failed with status code:", response.status_code)
    
    # get voice id that matches bot_name
    voice_id = None
    for voice in response.json()['voices']:
        if voice["name"] == bot_name:
            voice_id = voice["voice_id"]
            break
    if voice_id == None:
        return (0, "No voice found for bot_name:", bot_name)
    
    # send request to convert text to speech
    print("Sending request to convert text to speech...")
    response = requests.post(url + "text-to-speech/" + voice_id, json={"text": message_text}, headers=headers)
    
    if response.status_code != 200:
        return (0, "Request failed with status code:", response.status_code)
    
    # write out audio file
    # NOTE, if we wanted, we could save to a unique file name and return that
    print("Writing audio file...")
    audiofilename = "maury_bot/database/synthesized_audio/audio.mp3"
    with open(audiofilename, 'wb') as out:
        out.write(response.content)

    return (1, audiofilename)