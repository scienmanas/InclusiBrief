import discord 
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import json
import datetime
import requests

# For genai functionality
import pathlib
import textwrap
import google.generativeai as genai

# Load the environment
load_dotenv()

# Get Discord Bot Token and API Key
API_KEY = os.getenv("GEMINI_API_KEY")
TOKEN = os.getenv("TOKEN")



# class Bot(commands.bot) :

#     def __init__(self) :
#         pass


def main() :
    # bot = Bot()
    # bot.run(TOKEN)


    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content("The opposite of hot is")
    print(response.text)





# Call the main function
# if __name__ == "__main__" :
main()