![](https://i-made.theworstme.me/ea0ad4.png)

[![](https://img.shields.io/discord/307640404071677962.svg)](https://discord.gg/PEW4wx9) [![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/772/badge)](https://bestpractices.coreinfrastructure.org/projects/772)
[![](https://img.shields.io/badge/add%20bot-official%20instance-blue.svg)](https://discordapp.com/api/oauth2/authorize?client_id=272549225454239744&scope=bot&permissions=0)

# lolbot
Hi! This is the repository for lolbot, a Discord bot project

## Progress on rewrite
- [ ] Cogs
    - [x] common
    - [ ] fun
        - [x] cat [1]
        - [x] httpcat [1]
        - [x] dog [1]
        - [x] lizard [1]
        - [x] why
        - [x] robohash [1]
        - [ ] 8ball
        - [x] spin
        - [ ] yesno
        - [ ] joke/dadjoke/awdad/dadpls/shitjoke/badjoke
        - [ ] sumfuk
        - [x] excuse/bofh/techproblem
    - [x] git
        - [x] gl/gitlab
        - [x] gh/github
    - [ ] minecraft
        - [ ] mcserver
    - [ ] osu (possibly up to be split into a seperate bot)
        - [ ] osu
    - [ ] owner
        - [ ] game
            - [ ] set
            - [ ] clear
        - [ ] shutdown
        - [ ] reboot
        - [ ] feedbackrespond
    - [ ] packages
        - [ ] pypi
        - [ ] crates
    - [ ] stats
        - [ ] poststats
        - [ ] fakeguild
            - [ ] join
            - [ ] leave
    - [ ] utility
        - [x] hello
        - [ ] uptime
        - [ ] ping
        - [ ] stats
        - [ ] invite
        - [ ] user
        - [ ] invinfo (maybe finally finish this?)
        - [ ] version
        - [ ] feedback
        - [ ] whois (rewrite this to not use tld list?)
    - [ ] wolfram
        - [ ] wa
    - [x] weather
        - [x] weather
    - [ ] youtube
        - [ ] youtube/yt (maybe finally finish this?)
- [x] API
- [x] Core

[1] Moved into a seperate `pictures` cog to avoid making the `fun` cog/category too bloated

## Before we start
If you do end up running this bot for yourself, please keep it to personal use only out of respect.

If you try to submit it to bot lists anyway, I'm sure they'll find out what it really is very quickly anyways, so just don't.

## Running
Requirements:
- Python 3 + pipenv (Python 3.7 minimum, latest recommended)
- Various Python packages
- A working internet connection
- A brain

1. Install packages - Without these, the bot will absolutely refuse to run as they contain necessary code for connecting to Discord, etc.
```bash
pipenv install
```

2. Edit config - The example config should hold your hand through most of this stuff.
```bash
cp config-example.yaml config.yaml
nano config.yaml
```

3. Try to launch the bot - Yeah, not much to say about this one.
```bash
pipenv run bot
```

4. (**HIGHLY RECOMMENDED**) Install the systemd service - Make maintenance easy with the lolbot systemd file - start, stop, restart at any time!
```bash
mkdir -p ~/.config/systemd/user
cp run/lolbot.service ~/.config/systemd/user
loginctl enable-linger
systemctl --user daemon-reload
systemctl --user enable lolbot # Optional: let lolbot start when your system does
systemctl --user start lolbot
```

### Credits
- [luna](https://github.com/lun-4) - Contributions & code
- [slice](https://github.com/slice) - Code
