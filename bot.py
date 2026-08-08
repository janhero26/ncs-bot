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
current_song = None


def get_stream_url(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    with yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


def play_next(error=None):
    global current_song

    if error:
        print(f"Playback error: {error}")

    if not queue:
        queue.extend(build_shuffled_queue())

    song = queue.pop(0)

    try:
        stream_url = get_stream_url(song["video_id"])
    except Exception as e:
        print(f"Failed to load '{song['title']}': {e}")
        play_next()
        return

    current_song = song
    print(f"Now playing: {song['title']}")
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


@bot.command(name="skip")
async def skip(ctx):
    if voice_client is None or not voice_client.is_playing():
        await ctx.send("Nothing is playing right now.")
        return

    voice_client.stop()
    await ctx.send("Skipped.")


@bot.command(name="nowplaying")
async def nowplaying(ctx):
    if current_song is None:
        await ctx.send("Nothing is playing right now.")
        return

    await ctx.send(f"Now playing: **{current_song['title']}**")


@bot.command(name="queue")
async def show_queue(ctx):
    if not queue:
        await ctx.send("The queue is empty (will reshuffle on next song).")
        return

    upcoming = queue[:10]
    lines = [f"{i + 1}. {song['title']}" for i, song in enumerate(upcoming)]
    message = "\n".join(lines)

    if len(queue) > 10:
        message += f"\n...and {len(queue) - 10} more."

    await ctx.send(f"**Upcoming:**\n{message}")


if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)