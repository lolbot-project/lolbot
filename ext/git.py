from discord.ext import commands
import urllib.parse
from utils.embed import get_embed

class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        of 1 use per 5 seconds to comply with the rules.
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
                embed.title = f'{repo} on {instance}'
                embed.description = f'*{desc}*\n:star: {stars} :fork_and_knife: {forks}\n:arrow_down: `{cmd}`'
                await ctx.send(embed=embed)
            elif r.status == 404:
                embed.title = 'Oops...'
                embed.description = 'That repository seems to not exist, or is private. Are you sure you typed it correctly?'
                await ctx.send(embed=embed)

