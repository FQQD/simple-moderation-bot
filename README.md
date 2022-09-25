
# Simple Moderation Bot

A simple moderation Discord bot written in Python with disnake.py for self hosting


## Installation

Follow these steps to install the bot on Ubuntu Server:

```bash
  sudo apt install python3 pip git screen nano -y
  git clone https://github.com/FQQD/simple-moderation-bot.git
  cd simple-moderation-bot
  mkdir warnings
  sudo chmod +x start.sh
  pip3 install disnake
  pip3 install aiofiles
```

Set up an application in the discord developer portal, if you don't know how, read

https://discordjs.guide/preparations/setting-up-a-bot-application.html

To invite the bot to your servers read this:

https://discordjs.guide/preparations/adding-your-bot-to-servers.html

Please note that you should turn on all intents for simplicity.

Now you need your Bot's token. You can find it in the "Bot" section of your Discord developer apllication. Copy the Token and put it into the main.py file:

```bash
nano main.py
```
![alt text](https://imgur.com/JFKhyvW.png)

Paste your Token into the selcted area and exit nano with CTRL+X

## Run
To run this bot, we're gonna be using "screen", so the bot still runs, even if we exit our ssh connection.
```bash
screen -S moderationbot ./start.sh
```
You now should see after short waiting, that your bot is online and ready to be used.
To detach the screen session, do CTRL+A and CTRL+D.
Its now safe to exit your ssh session.

To view all running screen session / bots, run:
```bash
screen -ls
```

To reattach the screen session / the bot, run:
```bash
screen -x moderationbot
```
## Features

Here are all the commands that the Bot is able to perform:

/credit

See the credits of the bots

/avatar

Show and download the profile picture of a user

/help

Show this a list of commands that everyone can user

/moderation ban

Ban members (Use Discord intern feature for message removal) (Needs Ban Permission)

/moderation kick

Kick members (Needs Kick Permission)

/moderation warn

Warn members

/moderation warnings

See all warnings of a member

/moderation removewarnings

Remove warnings of a member

/user info

See information about a member

/moderation help

Show a list of commands that require the "Moderate Members" Permission
## About this project
This is my first attempt to program a real bot, so please dont hate on the code too much.

I know - it's messy an probably should be done completly differently, but it's enough for me, since it just works.

I hope you still like it!

If you use it, please dont remove / edit out my credits out of the /credits command.
