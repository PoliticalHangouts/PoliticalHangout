import discord, datetime
from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot):
      self.bot=bot
      self.name="Verification category"

    @commands.command(
      name="verify",
      aliases=[
        'ver',
        'v',
      ],
      brief="Allows you to verify",
      description="Allows you to verify for the bot",
      usage=""
    )
    async def verify(self, ctx):
      await ctx.message.add_reaction('✅')

      response_string = ''
      message_obj = await ctx.author.send(
        embed=discord.Embed(
          description=f"```\nAre you 13 or older?```",
          color=discord.Colour.dark_purple()
        ).set_author(name="Verification").set_footer(text="Your response to this question will be recorded upon being sent in this channel.")
      )
      response = await self.bot.wait_for('message', check=lambda message: message.channel==message_obj.channel and message.author==ctx.author)
      response_string+=f'1. Are you 13 or older? - {response.content}'
      
      message_obj = await ctx.author.send(
        embed=discord.Embed(
          description=f"```\nWhat ideology fits your views best?```",
          color=discord.Colour.dark_purple()
        ).set_author(name="Verification").set_footer(text="Your response to this question will be recorded upon being sent in this channel.")
      )
      response = await self.bot.wait_for('message', check=lambda message: message.channel==message_obj.channel and message.author==ctx.author)
      response_string+=f'\n-\n2. What ideology fits your views best? - {response.content}'
      
      message_obj = await ctx.author.send(
        embed=discord.Embed(
          description=f"```\nAre you racist, sexist, homophobic, or transphobic in any ways?```",
          color=discord.Colour.dark_purple()
        ).set_author(name="Verification").set_footer(text="Your response to this question will be recorded upon being sent in this channel.")
      )
      response = await self.bot.wait_for('message', check=lambda message: message.channel==message_obj.channel and message.author==ctx.author)
      response_string+=f'\n-\n3. Are you racist, sexist, homophobic, or transphobic in any ways? - {response.content}'      

      message_obj = await ctx.author.send(
        embed=discord.Embed(
          description=f"```\nDo you agree to the rules?```",
          color=discord.Colour.dark_purple()
        ).set_author(name="Verification").set_footer(text="Your response to this question will be recorded upon being sent in this channel.")
      )
      response = await self.bot.wait_for('message', check=lambda message: message.channel==message_obj.channel and message.author==ctx.author)
      response_string+=f'\n-\n4. Do you agree to the rules? - {response.content}' 

      await ctx.author.send("Response recorded...")

      channel = self.bot.get_channel(871885447939371079)
      embed=discord.Embed(
        description=f"```{response_string}```",
        color=discord.Colour.dark_purple()
      ).set_author(name=f'{str(ctx.author.id)} - {ctx.author.name}#{ctx.author.discriminator}', icon_url=ctx.author.avatar_url).set_footer(text="Verification Response")
      embed.timestamp = datetime.datetime.utcnow()
      await channel.send(
        embed=embed
     )

    @commands.command(
      name="accept",
      brief="Accepts a user's verification response",
      description="Accepts a user's verification response and gives them the Member role.",
      usage="<member_id>"
    )
    async def accept(self, ctx, member_id):
      member = ctx.guild.get_member(int(member_id))
      role = discord.utils.get(ctx.guild.roles, id=806018376933048321)
      await member.add_roles(role)
      await ctx.send("```\nMember {} verified!```".format(member.display_name))

    @commands.command(
      name="reject",
      brief="Rejects a user's verification response",
      description="Reject's a user's verification response and kicks them",
      usage="<member_id>"
    )
    async def reject(self, ctx, member_id):
      member = ctx.guild.get_member(int(member_id))
      await member.kick(reason="Verification rejected.")
      await ctx.send("```\nMember {} verification rejected```".format(member.display_name))

def setup(bot):
  bot.add_cog(Verification(bot))
