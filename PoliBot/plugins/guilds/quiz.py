import typing
import discord
import random
import asyncio

from replit import db
from plugins.guilds.data import Guild
from discord.ext import commands

from discord_slash import cog_ext, SlashContext

guilds = [Guild(0xcf78b, "loyalty"), Guild(0x8bbff7, "creativity"), Guild(0xf79d8b, "empathy"), Guild(0xd58bf7, "abrasive")]

class Prompt:
  def __init__(
    self,
    pos: str,
    neg: str,
    question: str
  ) -> None:
    self.pos = pos
    self.neg = neg
    self.question=question

class EmbedField:
  def __init__(
    self,
    name: str,
    value: str
  ) -> None:
    self.name=name
    self.value=value

class Response:
  def __init__(
    self,
    values = typing.Tuple[int, int],
  ) -> None:
    self.values=values

def is_sorted(
  values: typing.List[typing.Tuple[int, Guild]]
) -> bool:
  for i in range(0, 3):
    if i == 3:
      break
    
    if values[i][0] > values[i+1][0]:
      continue
      
    else:
      return False
    
  return True
    
def sort(
  values: typing.List[typing.Tuple[int, Guild]]
) -> typing.List[typing.Tuple[int, Guild]]:
  previous_value = 0
  n = 0
  while True:
    for i in range(0, 3):
      if previous_value == 0:
        previous_value = values[i]
        n = i
        continue
      else:
        if values[i][0] > previous_value[0]:
          values[n], values[i] = values[i], values[n]
          n = i
          continue
        else:
          continue
    
    if is_sorted(values):
      break
    else:
      continue
  
  return values
        
    
def get_guild(
  values: typing.List[typing.Tuple[int, Guild]],
) -> Guild:
  #⇔(Σa/((a))*1.15/Σ∀(b, c, d)/((∀(b, c, d) m))) < 1) ⊃ ∃⊤   |   discrete math for algorithm
  #
  #a - guild in guild loop
  #
  #b, c, d - other guilds
  current_guild = 0
  
  values = sort(values)
  for value in values:
    current_guild= value
    for value_next in values.remove(value):
      if value[1].get_total_points()/len(value[1].members) / value_next[1].get_total_points()/len(value_next[1].members) > 1.5:
        next_guild = True
      else:
        continue
    if next_guild:
      continue
  
  return current_guild[1]
  
    
async def create_question(
  question_number: int,
  prompt: str,
  options: typing.List[str],
  fields: typing.List[EmbedField],
  time_limit: int,
  bot: commands.Bot,
  ctx: SlashContext,
  guild: Guild,
  values: typing.Dict[str, typing.Tuple[int, int]]
) -> Response:
  
  embed = discord.Embed(
    description="```\n{}```".format(
      prompt
    ),
    color=guild.colour
  ).set_author(name="Question {0} - {1}".format(
    question_number,
    time_limit
  ))
  for field in fields:
    embed.add_field(name=field.name, value=field.value, inline=False)
  
  message = await ctx.send(
    embed=embed
  )
  
  for option in options:
    message.add_reaction(option)
  
  await asyncio.sleep(2)
  
  response = await bot.wait_for(
    'reaction_add',
    time_limit,
    check=lambda reaction, user: reaction.message == message and reaction.emoji in options and reaction.user == ctx.author
  )
  
  return Response(
    values[response[0].emoji]
  )


class Quiz(commands.Cog):
  def __init__(
    self,
    bot: commands.Bot
  ) -> None:
    self.bot=bot
    
  @cog_ext.cog_slash(
    name="Quiz",
    description="Take a quiz to assign you to a guild based on given traits.",
  )
  async def _quiz(
    self,
    ctx: SlashContext
  ) -> None:
    
    question_number = 0
    
    options = [
      '1️⃣',
      '2️⃣',
      '3️⃣',
      '4️⃣',
      '5️⃣',
      '6️⃣',
      '7️⃣'
    ]
    
    fields = [
      EmbedField(options[0], "Strongly Agree"),
      EmbedField(options[1], "Agree"),
      EmbedField(options[2], "Mildly Agree"),
      EmbedField(options[3], "Unsure"),
      EmbedField(options[4], "Mildly Disagree"),
      EmbedField(options[5], "Disagree"),
      EmbedField(options[6], "Strongly Disagree")
    ]
    
    values = {
      options[0]: (4, -2),
      options[1]: (3, -1),
      options[2]: (1, 0),
      options[3]: (0, 0),
      options[4]: (0, 1),
      options[5]: (-1, 3),
      options[6]: (-2, 4)
    }
    
    time_limit = 45
    
    loyalty, creativity, empathy, abrasive = 0, 0, 0, 0
    
    prompts = [
      Prompt
    ]
    
    for prompt in prompts:
      question_number+=1
      response = create_question(
        question_number,
        prompt.question,
        options,
        fields,
        time_limit,
        self.bot,
        ctx,
        random.choice(guilds),
        values
      )
      
      if prompt.pos == "loyalty": loyalty+=response.values[0]
      if prompt.pos == "creativity": creativity+=response.values[0]
      if prompt.pos == "empathy": empathy+=response.values[0]
      if prompt.pos == "abrasive": abrasive+=response.values[0]
        
      if prompt.neg == "loyalty": loyalty-=response.values[1]
      if prompt.neg == "creativity": creativity-=response.values[1]
      if prompt.neg == "empathy": empathy-=response.values[1]
      if prompt.neg == "abrasive": abrasive-=response.values[1]
      
      
    guild = get_guild([(loyalty, guilds[0]), (creativity, guilds[1]), (empathy, guilds[2]), (abrasive, guilds[3])])
    
    await ctx.send(
      file = discord.File('assets/guilds/{}.png'.format(guild.name), filename="{}.png".format(guild.name), spoiler=False),
      embed=discord.Embed(
        description="You got {}!",
        color=guild.colour
      ).set_author(
        name="Guild decided!"
      ).set_image(url="attachment://{}.png".format(guild.name))
    )
    
    guild.add_member(
      ctx.author
    )
    
    return
  
def setup(
  bot: commands.Bot
) -> None:
  bot.add_cog(Quiz(bot))
