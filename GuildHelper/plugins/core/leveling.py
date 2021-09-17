import discord
from discord.ext import commands

from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement

embed = discord.Embed(color=discord.Color.dark_purple())
embed.set_author(name=LevelUpAnnouncement.Member.name, icon_url=LevelUpAnnouncement.Member.avatar_url)
embed.description = f'Congrats {LevelUpAnnouncement.Member.mention}! You are now level {LevelUpAnnouncement.LEVEL}'

announcement = LevelUpAnnouncement(embed)

lvl = DiscordLevelingSystem(rate=1, per=60.0, level_up_announcement=announcement)
lvl.connect_to_database_file(r'data/DiscordLevelingSystem.db')

class Leveling(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Leveling category:"

  @commands.Cog.listener()
  async def on_message(self, message):
    await lvl.award_xp(amount=[15, 25], message=message)

  @commands.command(
    name="rank",
    aliases=[
      'level'
    ],
    brief="Displays a user's level",
    description="Displays a user's level, rank, and xp",
    usage="<member: optional>"
  )
  async def _rank(self, ctx, member: discord.Member=None):
    if member == None:
      member=ctx.author
    data = await lvl.get_data_for(member)
    await ctx.send(
      embed=discord.Embed(
        description=f"```\nMember - {member.display_name}\nLevel - {data.level}\nRank - {data.rank}\n```",
        color=discord.Colour.dark_purple()
      ).set_author(name="User Rank")
    )

  @commands.command(
    name="leaderboard",
    aliases=[
      'nolifes',
      'nl',
      'lb',
      'no-lifes'
    ],
    brief="Displays the guild's leveling leaderboard",
    description="Displays the guild's leaderboard for leveling",
    usage=''
  )
  async def _leaderboard(self, ctx):
    data = await lvl.each_member_data(ctx.guild, sort_by='rank')
    n = 10
    string = ''
    for item in data:
      string+=f'{11-n}.) {item.name} - Level: {item.level} - EXP: {item.xp}\n'
      n-=1
    await ctx.send(
      embed=discord.Embed(
        description=f"```\n{string}```",
        color=discord.Colour.dark_purple()
      ).set_author(name="Leaderboard")
    )

def setup(bot):
  bot.add_cog(Leveling(bot))
