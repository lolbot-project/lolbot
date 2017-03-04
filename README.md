![](https://lold.s-ul.eu/MqKR7DKI)
The only-one-file Discord bot made for fun.
Always WIP, always will be until its death, which I hope will never happen...

[lolbot official site](https://lolbot.banne.club) 
[<img src="https://discordapp.com/api/guilds/237379086970781698/widget.png?style=shield">](https://discord.gg/DCagZUP)

# Requirements

- Python 3.6 (I used pyenv for this, but Ubuntu has python3.6 PPAs. For other distros: YMMV)
- pip packages in requirements.txt (use `pip install -r requirements.txt` to install them automagically!)
- token for API ([Get it here](https://discordapp.com/developers/applications))

# Running

Pretty simple.

Change the token in config.json to yours, the bot will use it due to its JSON Parsing Technology(tm)!

You have to do nothing else except run `python3.6 index.py`

By default, lolbot's prefix is `^`. Change `command_prefix` to change the prefix:

`bot = commands.Bot(command_prefix='yourprefixhere', description=description)`

Have fun with lolbot!
