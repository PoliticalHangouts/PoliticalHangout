import discord
import os

from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(
  command_prefix="$",
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

slash = SlashCommand(bot)

def main() -> None:
  cogs = [
    'plugins.core.error.error_handling',
    'plugins.core.startup.login',
    'plugins.guilds.quiz',
    #'plugins.guilds.guilds',
    'plugins.debates.debate',
  ]
  for cog in cogs:
    bot.load_extension(cog)
    
  bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
  main()
