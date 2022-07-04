import random
from discord.ext import commands

# keys are the slap actions; values denote how many random server members need to be selected for the command
slap_actions = {
    "{} managed to avoid the slap. Good job!": 0,
    "{} cocked back their arm, and smacked {} right across the face.": 1,
    "{} swung their arm to slap {}, but they missed and fell to the ground. How embarrassing.": 1,
    "{} went to unload a huge slap on {}, but missed them and hit {} instead. Task successfully failed.": 2,
}


class Slap(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    def number_human_members(ctx):
        human_members = 0
        for member in ctx.guild.members:
            if not member.bot:
                human_members += 1

        return human_members

    @commands.command(help="Gets a random slap action. Actions may involve up to 2 other members in the server.")
    async def slap(self, ctx):
        numHumans = self.number_human_members(ctx)
        if numHumans < 3:           # If there aren't at least 3 people in the server, then just pick the first item in the action dict
            entry = list(slap_actions.items())[0]
        else:
            entry = random.choice(list(slap_actions.items()))

        numMembers = entry[1]

        if numMembers == 0:
            await ctx.send(entry[0].format(ctx.author.display_name))
        elif numMembers == 1:
            other_person = random.choice(ctx.guild.members)
            while other_person.bot or other_person == ctx.author:
                other_person = random.choice(ctx.guild.members)

            await ctx.send(entry[0].format(ctx.author.display_name, other_person.display_name))
        elif numMembers == 2:
            person_one = random.choice(ctx.guild.members)
            while person_one.bot or person_one == ctx.author:
                person_one = random.choice(ctx.guild.members)

            person_two = random.choice(ctx.guild.members)
            while person_two.bot or person_two == ctx.author or person_two == person_one:
                person_two = random.choice(ctx.guild.members)

            await ctx.send(entry[0].format(ctx.author.display_name, person_one.display_name, person_two.display_name))


async def setup(client):
    await client.wait_until_ready()
    client.add_cog(Slap(client))