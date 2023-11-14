import json
import os
import nextcord
import nextwave
from cooldowns import CallableOnCooldown
from nextcord import Intents
from nextcord.ext.commands import Bot
from nextcord.utils import get
import datetime
from bot.cogs import register_all_cogs
from bot.database.models import register_models
from bot.misc import Config


def start_bot():
    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = Bot(Config.CMD_PREFIX, intents=intents)

    register_all_cogs(bot)
    register_models()

    @bot.event
    async def on_ready():
        bot.loop.create_task(node_connect())

    async def node_connect():
        await bot.wait_until_ready()
        await nextwave.NodePool.create_node(bot=bot, host='lava.link', port=80, password='dismusic')

    @bot.event
    async def on_nextwave_node_ready(node: nextwave.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @bot.event
    async def on_message(message):
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
    async def on_application_command_error(interaction: nextcord.Interaction, error):
        error = getattr(error, "original", error)

        if isinstance(error, CallableOnCooldown):
            total_seconds = round(error.retry_after)
            minutes, seconds = divmod(total_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            embed = nextcord.Embed(
                title='❌ Ви дуже часто використовуєте цю команду!',
                description=f'Спробуйте ще раз через: {days}:{hours}:{minutes}:{seconds}.',
                color=nextcord.Color.dark_purple())
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)

        else:
            raise error

    @bot.event
    async def on_member_join(member):
        role = get(member.guild.roles, id=1003708592333000746)
        await member.add_roles(role)
        embed = nextcord.Embed(title='Ласкаво просима до нашого серверу ALCON!',
                               description='Тут ти знайдеш з ким пограти в сумний, дощовий та сірий день.',
                               color=nextcord.Color.dark_purple())
        embed.set_footer(text=member.name)
        embed.add_field(name='Ознайомся з правилами, та гайда грати! Поширюй українське.',
                        value='Разом до перемоги! Слава Україні! 💙💛')
        embed.set_image(
            url='https://media.discordapp.net/attachments/1016748092810346507/1039940489778049034/banner.png')
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        await member.send(embed=embed)
        emb = nextcord.Embed(title=f'👋Ласкаво просимо!',
                             description=f'**{member.mention}, ти став новим учасником нашої спільноти! ALCON**',
                             color=nextcord.Color.dark_purple())
        emb.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        channel = bot.get_channel(1003697879615033464)
        await channel.send(embed=emb)

    @bot.event
    async def on_member_remove(member):
        embed = nextcord.Embed(title=f'Дякуємо тобі, що був з нами!',
                               description=f'{member.mention}, сподіваємось це був гарно витрачений час.',
                               color=nextcord.Color.dark_purple())
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        channel = bot.get_channel(1003697879615033464)
        await channel.send(embed=embed)

    bot.run(os.environ.get('TOKEN'))
