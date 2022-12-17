
import os
import openai
import json

def chatgpt3(prompt):
    # get api key from config.json
    with open("config.json") as file:
        data = json.load(file)
        openai.api_key = data["openai_api_key"]

    # openai.Completion.create("This is a test", model="davinci:2020-05-03", stop=["\n", " Human:", " AI:"])

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
    # wait for a response
    # async with openai.Completion.create(**kwargs) as response:
    #     # ret the response
    #     print(response)
    #     print("Done!")
    #     ret = response["choices"][0]["text"]

    #     # clean text of newline chars
    #     ret = ret.replace("\n", "")
    #     ret = ret.replace("  ", " ")
    #     await ret
    response = openai.Completion.create(**kwargs)
    # ret the response
    print(response)
    print("Done!")
    ret = response["choices"][0]["text"]

    # clean text of newline chars
    ret = ret.replace("\n", "")
    ret = ret.replace("  ", " ")
    return ret