![](https://i-made.theworstme.me/ea0ad4.png)

[![](https://img.shields.io/discord/307640404071677962.svg)](https://discord.gg/PEW4wx9) [![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/772/badge)](https://bestpractices.coreinfrastructure.org/projects/772)
[![](https://img.shields.io/badge/add%20bot-official%20instance-blue.svg)](https://discordapp.com/api/oauth2/authorize?client_id=272549225454239744&scope=bot&permissions=0)

# lolbot
Hi! This is the repository for lolbot, a Discord bot project

## Progress on rewrite
- [] Cogs
    - [x] common
    - [] fun
    - [] git
    - [] minecraft
    - [] osu
    - [] owner
    - [] packages
    - [] stats
    - [] utility
    - [] wolfram
    - [] weather
    - [] youtube
- [] API (somewhat done, needs config stuff)
- [x] Core


## Before we start
If you do end up running this bot for yourself, please keep it to personal use only out of respect.

If you try to submit it to bot lists anyway, I'm sure they'll find out what it really is very quickly anyways, so just don't.

## Running
Requirements:
- Python 3 + pip (3.7 minimum, latest recommended)
- Various Python packages
- A working internet connection
- A brain
- Some sort of Linux[1]


(Note: I assume your Python 3 is the binary `python3`. Change instructions to suit your environment if needed.)

(I'll also assume the associated pip install is `pip3`.)

1. (**HIGHLY RECOMMENDED**) Create a virtual environment - This contains all the required packages in one directory and makes cleanup very simple if you decide to just delete this one day.
```bash
python3 -m venv env
source env/bin/activate
```

2. Install packages - Without these, the bot will absolutely refuse to run as they contain necessary code for connecting to Discord, etc.
```bash
pip3 install -Ur requirements.txt
```

3. Edit config - The example config should hold your hand through most of this stuff.
```bash
cp config-example.yaml config.yaml
nano config.yaml
```

4. Try to launch the bot - Yeah, not much to say about this one.
```bash
python bot.py
```

5. (**HIGHLY RECOMMENDED**) Install the systemd service - Make maintainence easy with the lolbot systemd file - start, stop, restart at any time!
```bash
mkdir -p ~/.config/systemd/user
cp run/lolbot.service ~/.config/systemd/user
loginctl enable-linger
systemctl --user daemon-reload
systemctl --user enable lolbot
# ^ Make lolbot launch on system startup, optional
systemctl --user start lolbot
```

[1] lolbot can probably be used on Windows provided you remove uvloop from requirements, but it's definitely not recommended

### Credits
- [luna](https://github.com/lnyaa) - Contributions & code
- [slice](https://github.com/slice) - Code
