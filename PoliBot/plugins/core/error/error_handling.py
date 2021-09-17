import discord
from discord.ext import commands
from discord_slash import SlashContext

from discord_slash.error import CheckFailure

class CommandError(commands.Cog, name="Command Error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, exception) -> None:
        
        #listens for Slash Command check failures (similiar to CommandNotFound)
        if isinstance(exception, CheckFailure):
            return

        await ctx.send(
          embed=discord.Embed(
            description="```\n{}```".format(exception),
            color=discord.Colour.red()
          ).set_author(
            name="Bot error."
          )
        )
          
        self.bot.logger.exception(f"ERROR: {exception}", exc_info=exception)


def setup(bot):
    bot.add_cog(CommandError(bot))
