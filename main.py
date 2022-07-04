import discord
from discord.ext import commands
import logging
from quart import Quart
from quart import request
import feedparser

import config
import music
import weather
import slap
import sports

logging.basicConfig(level=logging.INFO)
cogs = [music, weather, slap, sports]
client = commands.Bot(command_prefix="$", intents=discord.Intents.all(), case_insensitive=True)
videos = []     # keep track of the videos that we have gotten YT notifications fof


@client.event
async def on_ready():
    print("Pretender bot reporting for duty!")


app = Quart(__name__)


@app.route("/callback", methods=['POST', 'GET'])
async def callback():
    challenge = request.args.get("hub.challenge")

    if challenge:
        return challenge

    xml_data = feedparser.parse(await request.data)

    if xml_data.get("entries"):
        channel = client.get_channel(914638854819053619)
        video_url = xml_data['entries'][0]['link']

        # YouTube likes to send multiple Atom notifications for the same upload, so keep track of the videos that we
        # have seen so that Discord doesn't get spammed with links to the same video
        if video_url not in videos:
            videos.append(video_url)
            await channel.send(f"A new video was posted on Youtube: {video_url}")

    return " ", 204

for i in range(len(cogs)):
    client.loop.create_task(cogs[i].setup(client))

client.loop.create_task(app.run_task())
client.run(config.BOT_TOKEN)