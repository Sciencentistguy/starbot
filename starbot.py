import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', description="a starbot theoretically")


@bot.event
async def on_raw_reaction_add(event):
    reactchannel = bot.get_channel(event.channel_id)
    message = await reactchannel.fetch_message(event.message_id)
    await star_post_check(message)


async def star_post_check(message):
    if message.author == bot.user:
        return
    isstar = False
    best_of = discord.utils.get(message.guild.channels, name="best_of")
    for i in message.reactions:
        if i.emoji == ("⭐") and i.count >= 1 and message.channel != best_of:
            isstar = True
    if isstar:
        # embed message itself
        em = discord.Embed(title='Starred post', description=message.content, colour=0xFFD700)
        em.set_author(name=message.author, icon_url=message.author.avatar_url)
        try:
            if message.content.startswith('https://'):
                em.set_image(url=message.content)
        except:
            pass
        try:
            attach = message.attachments
            em.set_image(url=attach[0].url)
        except:
            pass
        # sending actual embed
        await best_of.send(embed=em)
        print("* Starred "+str(message.id)+" by "+message.author.display_name)


@bot.command(help="Rechecks all channels.")
async def recheck(ctx):
    messagecount = 0
    channelcount = 0
    guildcount = 0
    for guild in bot.guilds:
        print("\t Checking " + guild.name)
        for channel in guild.text_channels:
            print("Checked " + channel.name)
            try:
                async for message in channel.history(limit=None, before=None, after=None, around=None):
                    await star_post_check(message)
                    messagecount += 1
                channelcount += 1
            except Exception as e:
                print(e)
                channelcount += 1
                print("\t\tERROR: Skipped a channel")
        guildcount += 1
    print(f"Finished checking {messagecount} messages in {channelcount} channels and {guildcount} guilds.")

description = "A star bot."
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name, bot.user.id)

bot.run(open("token.txt", "r").read().strip(), bot=True, reconnect=True)
