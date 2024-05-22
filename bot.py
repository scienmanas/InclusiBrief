import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import google.generativeai as genai
from colorama import Fore, Style


# Load the environment
load_dotenv()

# Get Discord Bot Token and API Key
API_KEY = os.getenv("GEMINI_API_KEY")
TOKEN = os.getenv("TOKEN")

class InclusiBrief(commands.Bot):
    def __init__(self):
        # Initialize the bot
        intents = discord.Intents.default()
        intents.messages = True  # To get notified when user sends message
        intents.message_content = True  # To read the contents of the message
        super().__init__(command_prefix='!', intents=intents)

        # Configure Gemini
        genai.configure(api_key=API_KEY)
        # Configure models
        self.text_model = genai.GenerativeModel('gemini-pro')
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')

    async def on_ready(self):
        print("Logged in as: {0.user}".format(self))

    async def on_message(self, message: discord.Message) -> None:

        if message.author == self.user:
            return
        
        # Get the command
        command = message.content.lower()
        print(f"{Style.BRIGHT}{Fore.YELLOW}{command}{Fore.RESET}{Style.RESET_ALL}")

        if command.startswith("!help") :
            await self.help(message=message)
        elif command.startswith('!project') :
            await self.project_info(message=message)
        
        elif command.startswith("!website:analyse") :
            await self.wesbite_suitability_analyser(messgae=message, text=command.split(" ")[1])
        elif command.startswith("!website:get_info") :
            await self.get_website_info(message=message, text=command.split(" ")[1])
        
    @staticmethod
    async def help(message) -> None :
        pass

    @staticmethod
    async def project_info(message) -> None :
        pass

    async def wesbite_suitability_analyser (self, messgae, text) -> None :

        # Custom prompt
        print(text)
        prompt = f"You need to parse the webiste: {text}, and check whether the website fits WCAG 2.2 guidlines of suitability to deaf, blind people. Return the suitability analysis if the website, only the results and keep the response short also the checking for the guilines should be strict."

        async with messgae.channel.typing():

            response = self.text_model.generate_content(prompt)
            text = response.text

            await messgae.channel.send(text)

    async def get_website_info(self, message, text) -> None :

        # Custom prompt
        print(text)
        prompt = f"You need to ping the website: {text}, check the status of website whether it is up or down. Give a brief overview what website is used for."

        async with message.channel.typing() :

            resonse = self.text_model.generate_content(prompt)
            text = resonse.text

            await message.channel.send(text)



def start_bot():
    # Start the Bot
    inclusiveBrief_bot = InclusiBrief()
    inclusiveBrief_bot.run(TOKEN)

if __name__ == "__main__":
    start_bot()