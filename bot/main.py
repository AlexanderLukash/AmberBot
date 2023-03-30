import nextcord
from nextcord import Intents, FFmpegPCMAudio
from nextcord.ext.commands import Bot
from nextcord.utils import get

from bot.cogs import register_all_cogs
from bot.database.models import register_models
from bot.misc import Env, Config


def start_bot():
    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = Bot(Config.CMD_PREFIX, intents=intents)

    register_all_cogs(bot)
    register_models()

    # Words
    slavauk = ['слава україні', 'слава украине', 'slava ukraini', 'glory to ukraine']
    slavanac = ['slava nacii', 'glory of the nation', 'слава нації', 'слава нации']
    ukponad = ['ukraine', 'украина', 'україна']

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)
        msg = message.content.lower()

        if msg.find('слава україні') != -1:
            await message.channel.send("💙 💛 **Героям слава!** 💙 💛")

        if msg.find('слава украине') != -1:
            await message.channel.send("💙 💛 **Героям слава!** 💙 💛")

        if msg.find('slava ukraini') != -1:
            await message.channel.send("💙 💛 **Героям слава!** 💙 💛")

        if msg.find('glory to ukraine') != -1:
            await message.channel.send("💙 💛 **Героям слава!** 💙 💛")

        if msg.find('slava nacii') != -1:
            await message.channel.send("💙 💛 **Смерть ворогам!** 💙 💛")

        if msg.find('glory of the nation') != -1:
            await message.channel.send("💙 💛 **Смерть ворогам!** 💙 💛")

        if msg.find('слава нації') != -1:
            await message.channel.send("💙 💛 **Смерть ворогам!** 💙 💛")

        if msg.find('слава нации') != -1:
            await message.channel.send("💙 💛 **Смерть ворогам!** 💙 💛")

        if msg.find('путин') != -1:
            await message.channel.send("💙 💛 **Хуйло!** 💙 💛")

        if msg.find('путін') != -1:
            await message.channel.send("💙 💛 **Хуйло!** 💙 💛")

        if msg.find('putin') != -1:
            await message.channel.send("💙 💛 **Хуйло!** 💙 💛")

    @bot.event
    async def on_member_join(member):
        role = get(member.guild.roles, id=1003708592333000746)
        await member.add_roles(role)
        embed = nextcord.Embed(title='Ласкаво просима до нашого серверу ALCON!',
                               description='Тут ти знайдеш з ким пограти в сумний, дощовий та сірий день.',
                               color=nextcord.Color.red())
        embed.set_footer(text=member.name)
        embed.add_field(name='Ознайомся з правилами, та гайда грати! Поширюй українське.',
                        value='Разом до перемоги! Слава Україні! 💙💛')
        embed.set_image(
            url='https://media.discordapp.net/attachments/1016748092810346507/1039940489778049034/banner.png')
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        await member.send(embed=embed)
        emb = nextcord.Embed(title=f'👋Ласкаво просимо!',
                             description=f'**{member.mention}, ти став новим учасником нашої спільноти! ALCON**',
                             color=nextcord.Color.red())
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        channel = bot.get_channel(1003697879615033464)
        await channel.send(embed=emb)

    @bot.event
    async def on_member_remove(member):
        embed = nextcord.Embed(title=f'Дякуємо тобі, що був з нами!',
                               description=f'{member.mention}, сподіваємось це був гарно витрачений час.',
                               color=nextcord.Color.red())
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        channel = bot.get_channel(1003697879615033464)
        await channel.send(embed=embed)


    bot.run('MTA0NzkzODQxMDM0Nzc2NTkxMQ.GYttDK.Uc45Fvl0bmB7E55ZpiZWHruH0bWBFQ3azO1UvQ')
