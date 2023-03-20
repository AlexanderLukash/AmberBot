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
                               colour=nextcord.Color.red())
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.channel.purge(limit=int(amount))
        await interaction.response.send_message(content='', embed=embed, ephemeral=True, delete_after=4)

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
                               colour=nextcord.Color.red())
        embed.add_field(name='Причина:', value=f'{reason}.')
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(content='', embed=embed, delete_after=20)
        await asyncio.sleep(2)
        await user.ban(reason=reason)

    @nextcord.slash_command(name=f'banned', description=f'💙 Заблокувати користувача 💛')
    async def banned(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title='Путин:',
                               description=f'',
                               colour=nextcord.Color.red())

        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        banned_users = interaction.guild.bans()
        async for entry in banned_users:
            embed.add_field(name='Причина:', value=f'**{entry.user.name}**')
        await interaction.response.send_message(content='', embed=embed, ephemeral=True, delete_after=30)

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
                               colour=nextcord.Color.red())
        embed.add_field(name='Причина:', value=f'{reason}.')
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(content='', embed=embed, delete_after=20)
        await asyncio.sleep(2)
        await user.kick(reason=reason)


def register_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__MainAdminCog(bot))