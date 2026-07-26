import discord
from discord.ext import commands

import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    channel = bot.get_channel(int(config.VOICE_CHANNEL_ID))
    if channel is None:
        print("Voice channel not found. Check VOICE_CHANNEL_ID in .env")
        return

    await channel.connect()
    print(f"Connected to voice channel: {channel.name}")


if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)