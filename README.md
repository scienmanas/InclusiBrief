# InclusiBrief

<p align="center">
  <img src="https://raw.githubusercontent.com/scienmanas/InclusiBrief/main/assets/logo.png" alt="Logo" width="200" height="200">
</p>

This is a discord bot developed for GDSC genai workshop. There are various features in the bot which automated many daily tasks as fell as some fun features. Check the Features section for more details.

## Folder Structure:

```bash
.
├── assets
│   └── logo.png
│   └── permissions.png
│── .env
│    ├── TOKEN=Your Discord Bot Token
│    ├── GEMINI_API_KEY=Your Gemini API Key
├── .gitignore
├── main.py
├── app.py
├── bot.py
├── monitor_and_restart.py
├── build.sh
├── Procfile
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation and Running:

1. Clone the repository using the following command:

```bash
git clone https://github.com/scienmanas/InclusiBrief.git
```

2. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

3. Either you can run locally or deploy it in a virtual private server, or you can configure an Arduino zero to do it, since the bot is not heavy.

4. Create a `.env` file in the root directory and add the following variables:

```bash
TOKEN=YOUT_DISCORD_BOT_TOKEN
GEMINI_API_KEY=Your Gemini API Key
```

5. In Testing/debugging phase :

```bash
python monitor_and_restart.py
```

## Deployment:

1. You can deploy the bot in a virtual private server or in a cloud platform like Heroku, AWS, etc.
2. This bot is deployed on render and cron-jobs is used to monitor the uptime.
3. To deployt in render:
   - `build command`:
     - ```bash
       ./build.sh
       ```
   - `run command`:
     - ```bash
       python main.py
       ```

## Features:

- A place informer, webiste anayser, images analyser by use of genai.

## Contributors:

1. [Manas](https://github.com/scienmanas)

## API Used:

1. [Gemini API](https://docs.gemini.com/)

## Note:

- The bot is not optimized and configures, so we advise you to create your own bot and configure it according to your needs by utilizing the code. use **`!help`** to get bot commands.

- Enable the intents so that it can read message events.

![Permissions](https://raw.githubusercontent.com/scienmanas/InclusiBrief/main/assets/permissions.png)

## Contributing: 

The repository is open for contribution. All types of contribution are acknowledged - raising a bug issue, recommending new features as well as updating the code base. Before updating the code base raise an issue of recoomendign new feature and then can raise a pull requesting with the mentioned issue id.

## License:

This project is licensed under the MIT License
