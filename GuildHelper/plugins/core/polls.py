import discord, datetime, utils
from discord.ext import commands

class QuickPoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name="Polling category:"

    @commands.command(pass_context=True)
    async def poll(self, ctx, question, *options: str):
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)

    @commands.command(pass_context=True)
    async def tally(self, ctx, id=None):
        poll_message = await ctx.channel.fetch_message(id)
        embed = poll_message.embeds[0]
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        print(f'unformatted{unformatted_options}')
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [self.bot.user.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(reactor.id)
        output = f"Results of the poll for '{embed.title}':\n" + '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await ctx.send(
          embed = discord.Embed(
            description=output,
            color=discord.Colour.dark_purple()
          )
        )

    @commands.command(
      name="open-response-poll",
      aliases=[
        'orp',
        'open_response_poll',
        'openresponsepoll'
      ],
      brief="Creates a poll that server members can respond to openly",
      description="Creates a poll that server members can dm the bot to respond to openly, logs will go tothe server staff anonymously."
    )
    async def open_response_poll(self, ctx, poll_name, poll_question: str):
      utils.create_poll(poll_name, poll_question)
      await ctx.send(
        embed=discord.Embed(
          description=f"```\n{poll_question}```",
          color=discord.Colour.dark_purple()
        ).set_author(name=poll_name).set_footer(text="If you want to respond, please do g!respond, followed by the name of the poll. For more information you can run g!help respond")
      )

    @commands.command(
      name="respond",
      aliases=[
        'rorp',
        'resp',
      ],
      brief="Allows you to respond to an open response poll",
      description="Allows you to respond anonymously to an open response poll.",
      usage="<poll_name>"
    )
    async def respond(self, ctx, poll_name: str):
      question = utils.get_poll(poll_name)
      message_obj = await ctx.author.send(
        embed=discord.Embed(
          description=f"```{question}```",
          color=discord.Colour.dark_purple()
        ).set_author(name=poll_name).set_footer(text="Your response will be recorded anonymously.")
      )
      response = await self.bot.wait_for('message', check=lambda message: message.channel==message_obj.channel and message.author==ctx.author)
      channel = self.bot.get_channel(871871944457338950)
      embed=discord.Embed(
        description=f"```{response.content}```",
        color=discord.Colour.dark_purple()
      ).set_author(name=poll_name).set_footer(text="Poll Response")
      embed.timestamp = datetime.datetime.utcnow()
      await channel.send(
        embed=embed
     )

def setup(bot):
    bot.add_cog(QuickPoll(bot))
