import discord
from discord.ext import commands
import yt_dlp

import config
from player import build_shuffled_queue, YTDL_FORMAT_OPTIONS, FFMPEG_OPTIONS

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = []
voice_client = None


def get_stream_url(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    with yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


def play_next(error=None):
    if error:
        print(f"Playback error: {error}")

    if not queue:
        queue.extend(build_shuffled_queue())

    song = queue.pop(0)
    print(f"Now playing: {song['title']}")

    stream_url = get_stream_url(song["video_id"])
    source = discord.FFmpegPCMAudio(stream_url, **FFMPEG_OPTIONS)

    voice_client.play(source, after=lambda e: play_next(e))


@bot.event
async def on_ready():
    global voice_client

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    channel = bot.get_channel(int(config.VOICE_CHANNEL_ID))
    if channel is None:
        print("Voice channel not found. Check VOICE_CHANNEL_ID in .env")
        return

    voice_client = await channel.connect()
    print(f"Connected to voice channel: {channel.name}")

    queue.extend(build_shuffled_queue())
    play_next()


if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)