# HoneyGuard

HoneyGuard is a simple Discord honeypot bot. After startup, it creates a
`not-general` channel, posts a warning message there, and automatically bans any
account that sends a message in that channel.

It is designed to help catch hijacked or hacked accounts that spam scams,
server invites, NSFW links, and other suspicious messages.

## Requirements

- Python 3.10 or newer
- A Discord account
- A Discord server where you have permission to add bots
- A bot with permissions to create channels, delete messages, and ban members

## Creating the Discord Bot

1. Open the Discord Developer Portal:
   https://discord.com/developers/applications
2. Click **New Application**.
3. Enter a name, for example `HoneyGuard`, and create the application.
4. Go to the **Bot** tab.
5. Click **Add Bot**.
6. In **Privileged Gateway Intents**, enable:
   - **Server Members Intent**
   - **Message Content Intent**
7. In the **Token** section, click **Reset Token** or **Copy Token**.
8. Open `HoneyGuard.py` and replace this line at the bottom:

```python
bot.run("token here")
```

with:

```python
bot.run("YOUR_BOT_TOKEN")
```

Do not share your bot token with anyone. The token works like a password for
your bot.

## Installation

Clone or download the project, then enter the project folder:

```bash
cd HoneyGuard
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

On Windows:

```bat
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Adding the Bot to Your Server

1. In the Discord Developer Portal, open your application.
2. Go to **OAuth2** -> **URL Generator**.
3. In **Scopes**, select:
   - `bot`
   - `applications.commands`
4. In **Bot Permissions**, select:
   - `Manage Channels`
   - `Manage Messages`
   - `Ban Members`
   - `Send Messages`
   - `Read Message History`
   - `View Channels`
5. Copy the generated URL, open it in your browser, and add the bot to your
   server.

You can also use the `Administrator` permission, but it is safer to grant only
the permissions the bot needs.

## Running the Bot

After setting the token and installing the dependencies, start the bot:

```bash
python HoneyGuard.py
```

If everything works, you should see a message similar to:

```text
Bot online: HoneyGuard#0000
```

The bot will automatically create the `not-general` channel on servers where it
has the required permissions.

## Data File

After startup, the bot creates this file:

```text
honeypot_channels.json
```

This file stores honeypot channel IDs and the total ban count. Do not delete it
if you want to keep the statistics and saved channel mappings.

## Support

Discord: https://discord.gg/79jVdbyazX

---

by @pewnie
