import discord, utils
from discord.ext import commands
from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement

bot = commands.Bot(
  command_prefix=utils.get_prefix,
  intents=discord.Intents.all(),
  self_bot=False,
  description="A discord bot made to handle the guild system for the Political Hangout discord server.",
  help_command=None,
  case_insensitive=True,
  owner_ids=[
    707643377621008447,
    479576984205131787,
    292484057139380225,
    750971217489428480,
    581850206853791755,
    867145519255781437,
    592510722647261204,
    767201711114420247,
    339436064039239680,
  ],
  strip_after_prefix=True,
)

@bot.command()
async def create_thread(ctx, name):
  thread = await ctx.channel.create_thread("name", message="Thread created!", reason="Bot said so")

if __name__ == '__main__':
  cogs = utils.parse_file('cogs.coglist')
  for cog in cogs:
    bot.load_extension(cog)

bot.run(utils.parse_file('token.secret'))
