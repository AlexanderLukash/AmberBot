from nextcord.ext import commands
from nextcord.ext.commands import Cog
import nextcord
from nextcord import SlashOption
from nextcord.ext.commands import Bot
import json


# todo: TeamCogs
class __TeamAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name=f'team_add', description=f'💙 Додати учасників команди 💛')
    @commands.has_role(1003716763034329088)
    async def team_add(self, interaction: nextcord.Interaction, member: nextcord.Member = SlashOption(
        name="учасник",
        description="обери того хто є учасником команди серверу")):

        file_name = "team_users.json"
        try:
            # Load current data from the file (if available)
            with open(file_name, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If no file is found, create an empty dictionary
            data = {}

        if str(member.id) in data:
            embed = nextcord.Embed(
                title='❌ Цей учасник вже є у списку:',
                description='Зараз ваш список виглядає так.',
                color=nextcord.Color.dark_purple())
            for user_name in data:
                embed.add_field(name='', value=f'<@{data[user_name][1]}>')

            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            data[member.id] = member.name, member.id

            # Записываем обновленные данные в файл
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)
            with open(file_name, 'r') as file:
                data = json.load(file)
            embed = nextcord.Embed(
                title='✅ Ви успішно додали нового учасника вашої команди:',
                description='Тепер список вашої команди виглядає так.',
                color=nextcord.Color.dark_purple())
            for user_name in data:
                embed.add_field(name='', value=f'<@{data[user_name][1]}>')

            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694434977/12_uogafz_nmyjfn.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(name=f'team_del', description=f'💙 Видалити учасників команди 💛')
    @commands.has_role(1003716763034329088)
    async def team_del(self, interaction: nextcord.Interaction, member: nextcord.Member = SlashOption(
        name="учасник",
        description="обери того, кого треба видалити")):

        file_name = "team_users.json"
        try:
            # Load current data from the file (if available)
            with open(file_name, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If no file is found, create an empty dictionary
            data = {}

            # Remove user information from the dictionary (if any)
        if str(member.id) in data:
            del data[str(member.id)]

            # Write the updated data to a file
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)
            embed = nextcord.Embed(
                title='✅ Ви успішно видалили учасника вашої команди:',
                description='Тепер список вашої команди виглядає так.',
                color=nextcord.Color.dark_purple())
            for user_name in data:
                embed.add_field(name='', value=f'<@{data[user_name][1]}>')

            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694434977/12_uogafz_nmyjfn.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(
                title='❌ Цей учасник не є учасником команди:',
                description='Зараз ваш список виглядає так.',
                color=nextcord.Color.dark_purple())
            for user_name in data:
                embed.add_field(name='', value=f'<@{data[user_name][1]}>')

            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(name=f'team', description=f'💙 Наша команда 💛')
    async def team(self, interaction: nextcord.Interaction):
        # Loading data from a file
        file_name = 'team_users.json'
        with open(file_name, 'r') as file:
            data = json.load(file)
        embed = nextcord.Embed(
            title='☕ Наша команда:',
            color=nextcord.Color.dark_purple())
        for user_name in data:
            embed.add_field(name='', value=f'<@{data[user_name][1]}>')

        embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694434977/12_uogafz_nmyjfn.png')
        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed, ephemeral=True)


def register_team_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__TeamAdminCog(bot))
