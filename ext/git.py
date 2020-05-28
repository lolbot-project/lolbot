from discord.ext import commands
import urllib.parse
from utils.embed import get_embed

class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def generate_description(cls, description, stars, forks, command):
        return f'*{description}*\n:star: {stars} :fork_and_knife: {forks}\n :arrow_down: {command}'

    @commands.command(aliases=["gitlab"])
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def gl(self, ctx, repo: str, instance: str = "gitlab.com"):
        """
        Displays information about a GitLab repository.
        Example:
        `^gl gitlab-org/gitlab-ce`

        If you would like, you can tell this command to query
        your own GitLab instance instead of gitlab.com:
        `^gl your-username/your-repository git.your-username.blah`

        This command uses the GitLab API, and is limited
        to 1 use per 5 seconds to comply with the rules.
        """
        repo = urllib.parse.quote_plus(repo)
        embed = get_embed()
        async with await self.bot.session.get(f"https://{instance}/api/v4/projects/{repo}") as r:
            if r.status == 200:
                r = await r.json()
                if r["description"] == "":
                    desc = "No description provided."
                else:
                    desc = r["description"]
                repo = repo.replace("%2F", "/")
                stars = r["star_count"]
                forks = r["forks_count"]
                cmd = f'git clone {r["http_url_to_repo"]}'
                if instance == 'gitlab.com':
                    embed.title = f'{repo} on GitLab'
                else:
                    embed.title = f'{repo} on {instance}'
                embed.description = self.generate_description(desc, stars, forks, cmd)
            elif r.status == 404:
                embed.title = 'Oops...'
                embed.description = 'That repository doesn\'t seem to exist, or is private. Are you sure you typed it correctly?'
            await ctx.send(embed=embed)

    @commands.command(aliases=["github"])
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def gh(self, ctx, repo: str):
        """
        Displays information about a GitHub repository.
        Example:
        `^gh github/hub`

        This command uses the GitHub API, and is limited
        to 1 use per 5 seconds to comply with the rules.
        """
        embed = get_embed()
        async with await self.bot.session.get(f"https://api.github.com/repos/{repo}") as r:
            if r.status == 200:
                r = await r.json()
                if r["description"] == "":
                    desc = "No description provided."
                else:
                    desc = r["description"]
                stars = r["stargazers_count"]
                forks = r["forks_count"]
                cmd = f'git clone {r["clone_url"]}'
                embed.title = f'{repo} on GitHub'
                embed.description = self.generate_description(desc, stars, forks, cmd)
            elif r.status == 404:
                embed.title = 'Oops...'
                embed.description = 'That repository doesn\'t seem to exist, or is private. Are you sure you typed it correctly?'
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Git(bot))