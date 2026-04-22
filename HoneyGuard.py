# -*- coding: utf-8 -*-
# by @pewnie
# https://discord.gg/79jVdbyazX

import nextcord
from nextcord.ext import commands
import json
import os

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(intents=intents)

CHANNEL_NAME = "not-general"
DATA_FILE = "honeypot_channels.json"
WARNING_MESSAGE = (
    ":warning: **WARNING** :warning:\n\n"
    "This channel is used to **catch hacked/hijacked accounts**.\n"
    "Anyone who sends a message here will be **immediately banned**.\n\n"
    "**Do not write anything here.**"
)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"channels": {}, "total_bans": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_channel_id(guild_id: int):
    return load_data()["channels"].get(str(guild_id))

async def update_status():
    data = load_data()
    bans = data.get("total_bans", 0)
    await bot.change_presence(activity=nextcord.Game(name=f"Catched Accs: {bans}"))

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    for guild in bot.guilds:
        await setup_channel(guild)
    await update_status()

@bot.event
async def on_guild_join(guild):
    await setup_channel(guild)

async def setup_channel(guild):
    data = load_data()
    saved_id = data["channels"].get(str(guild.id))

    if saved_id:
        channel = guild.get_channel(saved_id)
        if channel:
            return

    overwrites = {
        guild.default_role: nextcord.PermissionOverwrite(
            view_channel=True,
            read_messages=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True,
            mention_everyone=False
        ),
        guild.me: nextcord.PermissionOverwrite(
            view_channel=True,
            read_messages=True,
            send_messages=True,
            manage_messages=True,
            ban_members=True,
            read_message_history=True
        )
    }

    channel = await guild.create_text_channel(
        CHANNEL_NAME,
        overwrites=overwrites,
        category=None
    )
    data["channels"][str(guild.id)] = channel.id
    save_data(data)

    msg = await channel.send(WARNING_MESSAGE)
    await msg.pin()
    print(f"Honeypot created on {guild.name}: #{channel.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    saved_id = get_channel_id(message.guild.id)
    if message.channel.id != saved_id:
        await bot.process_commands(message)
        return

    guild = message.guild
    member = message.author

    try:
        await message.delete()
    except:
        pass

    try:
        await guild.ban(
            member,
            reason="Wrote in honeypot channel (not-general)",
            delete_message_seconds=86400
        )

        data = load_data()
        data["total_bans"] += 1
        save_data(data)

        await update_status()
        print(f"Banned: {member} on {guild.name} | Total: {data['total_bans']}")
    except nextcord.Forbidden:
        print(f"Missing permissions to ban {member} on {guild.name}")
    except Exception as e:
        print(f"Error: {e}")

@bot.slash_command(name="support", description="Get support server link")
async def support(interaction: nextcord.Interaction):
    await interaction.response.send_message(
        "Join our support server: https://discord.gg/79jVdbyazX",
        ephemeral=True
    )


bot.run("PASTE TOKEN HERE")