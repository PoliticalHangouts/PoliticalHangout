import discord, asyncio, utils
from discord.ext import commands

from discordLevelingSystem import DiscordLevelingSystem

lvl = DiscordLevelingSystem(rate=1, per=60.0)
lvl.connect_to_database_file(r'data/DiscordLevelingSystem.db')

class Guilds(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Guilds Category"

  @commands.command(
    name="guild-quiz",
    aliases=[
      'gq',
      'guildquiz',
      'guild_quiz'
    ],
    brief="Helps you decide what guild to join",
    description="A quiz built to help you decide what guild is best for you.",
    usage=""
  )
  async def guild_quiz(self, ctx):
    rational = 0
    emotional = 0
    courageous = 0
    cunning = 0
    reactions = [
      '🇹',
      '🇫'
    ]
    await ctx.author.send(
      embed=discord.Embed(
        description="```Guild Personality Quiz v1.0```",
        color=discord.Colour.dark_purple()
      ).set_footer(text="Keep in mind all results are not necessarily indicative of the guild you need to join, instead they serve only as recommendations.")
    )
    
    
    question_1 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nRationality triumphs over emotion in most situations.```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_1.add_reaction(reaction)
    await asyncio.sleep(3)
    question_1_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_1 and reaction.emoji in reactions)
    if question_1_response[0].emoji == '🇹':
      rational+=4
    elif question_1_response[0].emoji == '🇫':
      emotional+=4
    
    
    question_2 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nA person who chooses to fight for what they believe is right is ultimately stronger```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_2.add_reaction(reaction)
    await asyncio.sleep(3)
    question_2_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_2 and reaction.emoji in reactions)
    if question_2_response[0].emoji == '🇹':
      courageous+=4
      emotional+=1
    elif question_2_response[0].emoji == '🇫':
      cunning+=4
      rational+=2
    
    
    question_3 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nIt is better to overthing than to not think at all```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_3.add_reaction(reaction)
    await asyncio.sleep(3)
    question_3_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_3 and reaction.emoji in reactions)
    if question_3_response[0].emoji == '🇹':
      cunning+=3
      rational+=2
    elif question_3_response[0].emoji == '🇫':
      courageous+=2
      emotional+=3
    
    
    question_4 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nYou are often good at staying calm under a lot of pressure.```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_4.add_reaction(reaction)
    await asyncio.sleep(3)
    question_4_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_4 and reaction.emoji in reactions)
    if question_4_response[0].emoji == '🇹':
      courageous+=5
      rational+=2
    elif question_4_response[0].emoji == '🇫':
      emotional+=4

    question_5 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nYou work for your own goals at all times. The opinions of others have no real effect on your actions.```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_5.add_reaction(reaction)
    await asyncio.sleep(3)
    question_5_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_5 and reaction.emoji in reactions)
    if question_5_response[0].emoji == '🇹':
      cunning+=4
      emotional-=1
    elif question_5_response[0].emoji == '🇫':
      emotional+=1
      courageous+=3


    question_6 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nYou value ends over means.```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_6.add_reaction(reaction)
    await asyncio.sleep(3)
    question_6_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_6 and reaction.emoji in reactions)
    if question_6_response[0].emoji == '🇹':
      cunning+=3
    elif question_6_response[0].emoji == '🇫':
      courageous+=2
      emotional+=1

    question_7 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nYou are often inclined to act with motive```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_7.add_reaction(reaction)
    await asyncio.sleep(3)
    question_7_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_7 and reaction.emoji in reactions)
    if question_7_response[0].emoji == '🇹':
      rational+=4
      cunning+=3
    elif question_7_response[0].emoji == '🇫':
      emotional+=1

    question_8 = await ctx.author.send(
      embed = discord.Embed(
        description="```\n`You get more happiness from helping others than helping yourself.``",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_8.add_reaction(reaction)
    await asyncio.sleep(3)
    question_8_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_8 and reaction.emoji in reactions)
    if question_8_response[0].emoji == '🇹':
      emotional+=4
      courageous+=2
    elif question_8_response[0].emoji == '🇫':
      cunning+=2

    question_9 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nYou think the world would be a better place if people relied more on thought and reason than emotion.```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_9.add_reaction(reaction)
    await asyncio.sleep(3)
    question_9_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_9 and reaction.emoji in reactions)
    if question_9_response[0].emoji == '🇹':
      rational+=4
    elif question_9_response[0].emoji == '🇫':
      emotional+=1

    question_10 = await ctx.author.send(
      embed = discord.Embed(
        description="```\nPeople often don't know whats good for them, and so decisions need to be made for them```",
        color=discord.Colour.dark_purple()
      ).add_field(name="True", value="🇹").add_field(name="False", value="🇫")
    )
    for reaction in reactions:
      await question_10.add_reaction(reaction)
    await asyncio.sleep(3)
    question_10_response = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message==question_10 and reaction.emoji in reactions)
    if question_10_response[0].emoji == '🇹':
      cunning+=3
      rational+=2
    elif question_10_response[0].emoji == '🇫':
      emotional+=2

    #decision logic
    values = {
      'rational': rational,
      'cunning': cunning,
      'courageous': courageous,
      'emotional': emotional
    }
    highest_value = max(values, key=values.get)
    print(highest_value)
    if highest_value == 'rational':
      embed = utils.get_guild_embed('Sphinxes')
    

def setup(bot):
  bot.add_cog(Guilds(bot))
