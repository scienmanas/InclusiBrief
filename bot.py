import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import google.generativeai as genai
from colorama import Fore, Style
import requests
from PIL import Image
from io import BytesIO


# Load the environment
load_dotenv()

# Get Discord Bot Token and API Key
API_KEY = os.getenv("GEMINI_API_KEY")
TOKEN = os.getenv("TOKEN")

# Constants
PROJECT_URL = "https://github.com/scienmanas/InclusiBrief"
ERROR_MESSAGE = "An Unknown error occurred :("


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
        self.text_model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')

    async def on_ready(self):
        print("Logged in as: {0.user}".format(self))

    async def on_message(self, message: discord.Message) -> None:

        if message.author == self.user:
            return

        # Get the command
        command = message.content.lower()

        if command.startswith("!help"):
            await self.help(message=message)
        elif command.startswith('!project'):
            await self.project_info(message=message)

        elif command.startswith("!website:analyse"):
            await self.wesbite_suitability_analyser(messgae=message, text=command.split(" ")[1:])
        elif command.startswith("!website:get_info"):
            await self.get_website_info(message=message, text=command.split(" ")[1:])

        elif command.startswith("!vision:analyse_img"):
            await self.get_img_informtion(message=message)

        elif command.startswith("!place:inform"):
            await self.place_informer(message=message, text=command.split(" ")[1:])

    @staticmethod
    async def help(message) -> None:

        # Embedded message contents
        embed = discord.Embed(
            title="InclusiveBrief",
            description="Did someone call me ? 🧐",
            color=discord.Color.dark_magenta()
        )
        embed.add_field(
            name="About",
            value="Hi! I am an Miultipupose Bot capable to reading images, providing a brief description of it, and can server as a webiste informer.",
            inline=False
        )
        embed.add_field(
            name="Commands",
            value="To operate me, use **!<command>**\n"
                  "- **!help**: To view commands.\n"
                  "- **!website:analyse <website>**: To analyse whether a website is following WCAG 2.0 guidlines.\n"
                  "- **!website:get_info <website>**: To get information of a website.\n"
                  "- **!vision:analyse_img** with image attached: To get the information about image.\n"
                  "- **!place:inform <place>**: To ask bot to plan a trip at a place.",
            inline=False
        )
        embed.set_footer(
            text="This bot was developed by Manas"
        )

        await message.channel.send(embed=embed)

    @staticmethod
    async def project_info(message) -> None:

        text = f"The project can be found at url: {PROJECT_URL}"

        await message.channel.send(text)

    # This won't work -> Basically a linting functionality and in next we have feature to check it. (es-lint)

    async def wesbite_suitability_analyser(self, messgae, text) -> None:

        # Custom prompt
        prompt = f"You need to parse the webiste: {text}, and check whether the website fits WCAG 2.2 guidlines of suitability to deaf, blind people. Return the suitability analysis if the website, only the results and keep the response short also the checking for the guilines should be strict."

        try:

            async with messgae.channel.typing():

                response = self.text_model.generate_content(prompt)
                text = response.text

                await messgae.channel.send(text)
        except:

            await messgae.channel.send(ERROR_MESSAGE)

    async def get_website_info(self, message, text) -> None:

        # Custom prompt
        prompt = f"""Analyze the website: {text}

        **Here's what I'm looking for:**
        
        * **Purpose:** What is the main function or service offered by the website? Is it an e-commerce store, a news website, a portfolio, a blog, etc.?
        * **Content:** Briefly describe the type of content found on the website (e.g., articles, products, services, images, videos).
        * **Target Audience:** Who is the website aimed at? (e.g., businesses, general consumers, a specific niche)
        
        **Pay close attention to the website's metadata, including the title tag, meta description, and keywords.** This information can provide valuable clues about the website's purpose and target audience.
        
        **Keep the response concise and informative.**"""

        try:

            async with message.channel.typing():

                resonse = self.text_model.generate_content(prompt)
                text = resonse.text

                await message.channel.send(text)

        except:

            await message.channel.send(ERROR_MESSAGE)

    async def get_img_informtion(self, message) -> None:

        # Get image url
        if message.attachments:
            image_url = message.attachments[0]

        try:

            async with message.channel.typing():

                # Download and store images
                image_bytes = self.download_image(image_url)
                image = Image.open(BytesIO(image_bytes))

                # Get the image details from vision model
                response = self.vision_model.generate_content(image)
                text = response.text

                # Tailor the response received from the vision model by feeding it into text model
                prompt = f"""The following text is the response from a Gemini Vision model analyzing an image:

                {text}

                Please reformat this response into a clear and concise summary with the following structure:

                **Image:**

                * Briefly describe the main subject(s) in the image.

                **Details:**

                * Describe any interesting details or objects in the image.

                **Additional Notes:**

                * Include any relevant information not covered in the previous sections.
                """
                response = self.text_model.generate_content(contents=prompt)
                text = response.text

                await message.channel.send(text)

        except:

            await message.channel.send(ERROR_MESSAGE)

    async def place_informer(self, message, text):

        prompt = f"""Tell me about the culture, tourism, famous landmarks, and famous foods of {text}. Keep your response under 2000 characters. Don't ask any questions. Resposne Format: 
        
        **Culture:**
        * Describe the predominant cultural aspects and traditions.

        **Tourism:**
        * Highlight popular tourist attractions and activities.

        **Famous Landmarks:**
        * List renowned landmarks and their significance.

        **Famous Foods:**
        * Mention iconic dishes or culinary specialties.

        **Keep resposne under 1900 characters**
        """

        try:

            async with message.channel.typing():

                response = self.text_model.generate_content(contents=prompt)
                text = response.text

                await message.channel.send(text)

        except:

            await message.channel.send(ERROR_MESSAGE)

    @staticmethod
    def download_image(image_url):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                return response.content

            else:
                print("An unknown error occurred.")

        except requests.RequestException as e:

            print(f"Error downloading image: {e}")
            return None


def start_bot():
    # Start the Bot
    inclusiveBrief_bot = InclusiBrief()
    inclusiveBrief_bot.run(TOKEN)


if __name__ == "__main__":
    start_bot()
