import discord
from discord.ext import commands
import cogs.utils.gitapi as api
from cogs.utils.plainreq import get_req
import urllib.parse

class Git:
    def __init__(self, bot):
        self.bot = bot
        #self.ghkey = self.bot.config['github']
        self.dle = '<:download:455349673314484224>'
        #self.ghauth = {
        #    'Authorization': f'token {self.ghkey}',
        #    'Accept': 'application/vnd.github.mercy-preview+json'
        #}

    @commands.command(aliases=['gitlab'])
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def gl(self, ctx, repo: str, instance: str='gitlab.com'):
        """
        Grabs information about a GitLab repository.
        The syntax is written like this:
        `^gl gitlab-org/gitlab-ce

        If you would like, you can also use your
        own little GitLab instance to bring up
        your repo instead. Here's a example!
        `^gl user/repo your-gitlab-instance.com`

        This command uses GitLab's API, and has
        a ratelimit of 1 use per 5 seconds to
        comply with ratelimiting.
        """
        repo = urllib.parse.quote_plus(repo)
        rurl = api.gl_build(f'projects/{repo}')
        async with get_req(ctx.bot.session, rurl) as r:
            if r.status == 200:
                rj = await r.json()
                if rj['description'] == '':
                    desc = 'No description provided.'
                else:
                    desc = rj['description']
                stars = rj['star_count']
                forks = rj['forks_count']
                clone = 'git clone {rj["http_url_to_repo"]}'
                await ctx.send(embed=discord.Embed(title=f'{repo} on {instance}',
                                        description=f'*{desc}*\n'
                                        f':star: {stars} :fork_and_knife: {forks}\n'
                                        f'{self.dle} `{clone}`',
                                        colour=0x690E8))
            elif r.status == 404:
                await ctx.send(embed=discord.Embed(title='Oopsie woopsie!',
                                                   description='That repository'
                                                   'could not be found.',
                                                   colour=0x690E8))

    @commands.command(aliases=['github'])
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def gh(self, ctx, repo: str):
        """
        Grabs information about a GitHub repository.
        The syntax is written like this:
        `^gh github/hub`

        This command uses GitHub's API, and has
        a ratelimit of 1 use per 5 seconds to
        comply with ratelimiting.
        """

        rurl = api.gh_build(f'repos/{repo}')
        async with get_req(ctx.bot.session, rurl) as r:
            if r.status == 200:
                rj = await r.json()
                if rj['description'] == '':
                    desc = 'No description provided.'
                else:
                    desc = rj['description']
                stars = rj['stargazers_count']
                forks = rj['forks_count']
                clone = rj['clone_url']
                repo_em = discord.Embed(title=f'{repo}',
                                        description=f'*{desc}*\n'
                                        f':star: {stars} :fork_and_knife: {forks}\n'
                                        f'{self.dle} `git clone {clone}`',
                                        colour=0x690E8)
                await ctx.send(embed=repo_em)
            elif r.status == 404:
                repo_em = discord.Embed(title='Error',
                                        description='Repository not found.',
                                        colour=0x690E8)
                await ctx.send(embed=repo_em)


def setup(bot):
    bot.add_cog(Git(bot))
