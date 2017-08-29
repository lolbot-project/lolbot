
![](https://i-made.theworstme.me/ea0ad4.png)

[![](https://img.shields.io/badge/discord-server-7289DA.svg)](https://discord.gg/PEW4wx9) [![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/772/badge)](https://bestpractices.coreinfrastructure.org/projects/772)
[<img src="https://lold.s-ul.eu/OC314kET">](https://discordapp.com/api/oauth2/authorize?client_id=272549225454239744&scope=bot&permissions=0)

# Warning
Usually you shouldn't run a selfhost instance or clone of this bot. It requires some setup and this isn't a 1-2-3 bot. **Support will be limited. There is only so much I can do to support people. You may have to fix things yourself. Be warned.**

Also a tip:
  - Don't put selfhosts on Discord Bots. They're not your own bots and you shouldn't treat them like such. You only host it

So... do you wanna run it anyways?

If so... here's the little guide I put together.

## Requirements

- Python 3.6
- Some python modules (`pip install -Ur requirements.txt`)
- A text editor that isn't notepad or something
- Knowing how to actually maintain a bot

## Running

1. `git clone https://github.com/tilda/lolbot`
2. `cd lolbot`
3. `nano config.json` (follow the comments beginning with `//`)
4. `python3.6 index.py` 

Addendum 4a: use screen: `screen -DmS python3.6 index.py`

Addendum 4b: use pm2: `pm2 start index.py --name lolbot --interpreter python3.6` (this is currently used in production)

### Features probably never added
- music (maybe soon? - note from 8/28/17)
- something else (???)
