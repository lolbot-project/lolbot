import discord
from discord.ext import commands
import cogs.utils.ghapi as gh


class GitHub:
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.key = bot.config['github']
        self.ghauth = {
            'Authorization': f'token {self.key}',
            'Accept': 'application/vnd.github.mercy-preview+json'
        }

    @commands.command(aliases=['github'])
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def gh(self, ctx, repo: str):
        """
        Grabs information about a GitHub repository.
        This is the way you type in the command:
        `^gh github/hub`

        This is powered by GitHub's API.
        This command has a ratelimit of 1 command per 5 seconds.
        This is done to comply with GitHub's API ratelimits.
        """

        async with ctx.bot.session.get(gh.build_url(f'repos/{repo}'),
                                       headers=None) as r:
            if r.status == 200:
                rj = await r.json()
                desc = rj['description']
                stars = rj['stargazers_count']
                forke = '<a:forkconga:397940431025078272>'
                forks = rj['forks_count']
                dle = '<:download:423196305419141130>'
                clone = rj['clone_url']
                repo_em = discord.Embed(title=f'{repo}',
                                        description=f'*{desc}*\n'
                                        f':star: {stars} {forke} {forks}\n'
                                        f'{dle} `git clone {clone}`',
                                        colour=0x690E8)
                await ctx.send(embed=repo_em)
            elif r.status == 404:
                repo_em = discord.Embed(title='Error',
                                        description='Repository not found.',
                                        colour=0x690E8)
                await ctx.send(embed=repo_em)


def setup(bot):
    bot.add_cog(GitHub(bot))
