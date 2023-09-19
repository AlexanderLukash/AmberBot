import asyncio
from nextcord.ext.commands import Cog
from nextcord.ext import commands
import nextcord
from nextcord import SlashOption
from nextcord.ext.commands import Bot


# todo: AdminCogs
class __MainAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    # Clear messages
    @nextcord.slash_command(name=f'clear', description=f'💙 Очищає повідомлення з каналу 💛')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, interaction=nextcord.Interaction,
                    amount: int = SlashOption(
                        name="кількість",
                        description="за замовчуванням: 15",
                        default=15
                    )):
        embed = nextcord.Embed(title='✅ Успішно!',
                               description=f'Повідомлення успішно видалені. `` {amount} ``',
                               colour=nextcord.Color.dark_purple())
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694458613/clear_taku6z.png')
        await interaction.send(content='', embed=embed, ephemeral=True, delete_after=15)
        await interaction.channel.purge(limit=int(amount))

    # Ban user
    @nextcord.slash_command(name=f'ban', description=f'💙 Заблокувати користувача 💛')
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, user: nextcord.Member,
                  reason: str = SlashOption(
                      name="причина",
                      description="за що так з ним?",
                      default='За порушення🕸️'
                  )):
        embed = nextcord.Embed(title='✅ Успішно!',
                               description=f'Користувач **{user}** був заблокований.',
                               colour=nextcord.Color.dark_purple())
        embed.add_field(name='Причина:', value=f'{reason}.')
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.send(content='', embed=embed, delete_after=20)
        await asyncio.sleep(2)
        await user.ban(reason=reason)

    @nextcord.slash_command(name=f'banned', description=f'💙 Заблокувати користувача 💛')
    async def banned(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title='Заблоковані:',
                               description=f'',
                               colour=nextcord.Color.dark_purple())

        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        banned_users = interaction.guild.bans()
        async for entry in banned_users:
            embed.add_field(name='', value=entry.user.mention)
        await interaction.send(content='', embed=embed, ephemeral=True, delete_after=30)

    # Kick user
    @nextcord.slash_command(name=f'kick', description=f'💙 Кікнути користувача 💛')
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: nextcord.Interaction, user: nextcord.Member,
                   reason: str = SlashOption(
                       name="причина",
                       description="за що так з ним?",
                       default='За порушення🕸️'
                   )):
        embed = nextcord.Embed(title='✅ Успішно!',
                               description=f'Користувач **{user}** був кікнутий.',
                               colour=nextcord.Color.dark_purple())
        embed.add_field(name='Причина:', value=f'{reason}.')
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.send(content='', embed=embed, delete_after=20)
        await asyncio.sleep(2)
        await user.kick(reason=reason)

    @nextcord.slash_command(name=f'donate', description=f'💙 Пожертвування на сервер 💛')
    @commands.has_permissions(ban_members=True)
    async def donate(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        embed = nextcord.Embed(title='Підтримати наш проект 💸',
                               description=f'Це дозволить нам рости та розвиватися.',
                               colour=nextcord.Color.dark_purple())
        embed.add_field(name='БанкаMono:', value=f'https://send.monobank.ua/jar/85Vs9rq7vW', inline=False)
        embed.add_field(name='Номер Картки:', value=f'5375 4112 0673 2021', inline=False)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694676492/card_donate_ivoyol.png')
        embed.set_thumbnail(url='https://send.monobank.ua/img/money.png')
        await interaction.send(content=f'Повідомлення надіслано в канал: <#{channel.id}>', ephemeral=True)
        await channel.send(content='<@&1005778153349857290>', embed=embed)

    @nextcord.slash_command(name=f'social_media', description=f'💙 Наші соціальні медіа 💛')
    @commands.has_permissions(ban_members=True)
    async def social_media(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        embed = nextcord.Embed(title='Наші соціальні мережі 📢',
                               description=f'Підтримайте нас підпискою.',
                               colour=nextcord.Color.dark_purple())
        embed.add_field(name='TikTok:', value=f"https://www.tiktok.com/@amberua", inline=False)
        embed.add_field(name='YouTube:', value=f'https://www.youtube.com/@amberua', inline=False)
        embed.add_field(name='Discord:', value=f'https://discord.com/invite/e2HSn2kt7U', inline=False)
        embed.add_field(name='БанкаMono:', value=f'https://send.monobank.ua/jar/85Vs9rq7vW', inline=False)
        embed.add_field(name='', value=f'', inline=False)
        embed.add_field(name='Розвивай українське разом з AMBER :flag_ua:', value=f'', inline=False)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694962084/banner_media_b3uy1z.png')
        embed.set_thumbnail(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        await interaction.send(content=f'Повідомлення надіслано в канал: <#{channel.id}>', ephemeral=True)
        await channel.send(content='<@&1005778153349857290>', embed=embed)


def register_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__MainAdminCog(bot))
