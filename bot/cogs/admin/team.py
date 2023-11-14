from nextcord.ext import commands
from nextcord.ext.commands import Cog
import nextcord
from nextcord import SlashOption
from nextcord.ext.commands import Bot
import json

# define the filename for storing team user data
file_name = "team_users.json"


# loading current data
def load_data():
    try:
        # loading current data from a file (if the file exists)
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # if no file is found, create an empty dictionary
        data = {}

    return data


# write the updated data to the file
def save_data(data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


# data update function
def data_update(user_id, user_name):
    data = load_data()

    if str(user_id) in data:
        data = data
    elif user_id is None and user_name is None:
        data = data
    else:
        # if the user does not exist, create a new record
        data[user_id] = user_name, user_id

        # write the updated data to the file
        save_data(data)

        with open(file_name, 'r') as file:
            data = json.load(file)

        data = data

    return data


# todo: TeamCogs
class __TeamAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    # the function of adding a user to the team
    @nextcord.slash_command(name=f'team_add', description=f'💙 Додати учасників команди 💛')
    @commands.has_role(1003716763034329088)
    async def team_add(self, interaction: nextcord.Interaction, member: nextcord.Member = SlashOption(
        name="учасник",
        description="обери того хто є учасником команди серверу")):

        data = load_data()

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
            data = data_update(user_id=member.id, user_name=member.name)

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

    # the function of removing a user from the team
    @nextcord.slash_command(name=f'team_del', description=f'💙 Видалити учасників команди 💛')
    @commands.has_role(1003716763034329088)
    async def team_del(self, interaction: nextcord.Interaction, member: nextcord.Member = SlashOption(
        name="учасник",
        description="обери того, кого треба видалити")):

        data = load_data()

        # remove user information from the dictionary (if any)
        if str(member.id) in data:
            del data[str(member.id)]

            save_data(data)
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

    # function of displaying team members
    @nextcord.slash_command(name=f'team', description=f'💙 Наша команда 💛')
    async def team(self, interaction: nextcord.Interaction):
        data = load_data()
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


# function to register the team cog with the bot
def register_team_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__TeamAdminCog(bot))
