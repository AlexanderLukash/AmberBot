import json

import cooldowns
import nextcord
import requests
from nextcord import SlashOption, ButtonStyle
from nextcord.ext.commands import Bot
from nextcord.ext.commands import Cog
from nextcord.ui import Button, View

# todo: GitHubCogs

# define the filename for storing GitHub user data
file_name = "github_users.json"


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


# function to retrieve GitHub user information using the GitHub API
def get_github_info(user_login):
    url = f"https://api.github.com/users/{user_login}"
    response = requests.get(url)

    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        return None


# data update function
def data_update(user_id, user_name, git_info):
    data = load_data()
    user_info = git_info

    if str(user_id) in data:
        data[str(user_id)] = user_name, user_id, user_info['login'], \
            user_info[
                'followers'], user_info['public_repos'], user_info['starred_url'].count('{/repo}'), user_info[
            'avatar_url'], user_info['html_url'], user_info['created_at'][:10], user_info['location']
        save_data(data)

        with open(file_name, 'r') as file:
            data = json.load(file)

        data = data
    elif user_id is None and user_name is None:
        data = data
    else:
        # if the user does not exist, create a new record
        data[user_id] = user_name, user_id, user_info['login'], user_info[
            'followers'], user_info['public_repos'], user_info['starred_url'].count('{/repo}'), user_info[
            'avatar_url'], user_info['html_url'], user_info['created_at'][:10], user_info['location']

        # write the updated data to the file
        save_data(data)

        with open(file_name, 'r') as file:
            data = json.load(file)

        data = data

    return data


# class for the interactive "Delete" view
class GitDel(nextcord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Видалити", style=nextcord.ButtonStyle.green, emoji='🗑')
    async def profile_del(self):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Відмінити", style=nextcord.ButtonStyle.red, emoji='✖')
    async def profile_del_cansel(self):
        self.value = False
        self.stop()


# main class for the GitHub user commands
class __GitHubUserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    # function to handle server errors
    async def server_error(self, interaction):
        embed = nextcord.Embed(
            title='❌ Помилка на стороні серверу!',
            description='Не вдалося переглянути профіль GitHub. Спробуйте пізніше, або зверніться до адміністрації.',
            color=nextcord.Color.dark_purple())
        embed.set_image(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed, ephemeral=True)

    # slash command to add a GitHub profile
    @nextcord.slash_command(name=f'gitprofile', description=f'💙 Додати свій профіль GitHub 💛')
    async def github_add_profile(self, interaction: nextcord.Interaction, username=SlashOption(
        name="нікнейм",
        description="встав сюди свій github нікнейм")):

        user_info = get_github_info(user_login=username)

        if user_info:
            data = load_data()

            if str(interaction.user.id) in data:
                data = data_update(user_id=interaction.user.id, user_name=interaction.user.name, git_info=user_info)
                data = data[str(interaction.user.id)]
                embed = nextcord.Embed(
                    title='❌ Ти вже додав свій GitHub!',
                    description='Зараз твій профіль виглядає так.',
                    color=nextcord.Color.dark_purple())
                embed.set_author(name=f'{data[2]}', icon_url=f'{data[6]}')
                embed.add_field(name=f'Repositories: ', value=f'{data[4]}')
                embed.add_field(name='Followers: ', value=f'{data[3]}')
                embed.add_field(name='Stars: ', value=f'{data[5]}')
                embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
                embed.set_thumbnail(url=f'{data[6]}')
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await interaction.send(embed=embed, ephemeral=True)
            else:
                data = data_update(user_id=interaction.user.id, user_name=interaction.user.name, git_info=user_info)
                data = data[str(interaction.user.id)]
                embed = nextcord.Embed(
                    title='✅ Ви успішно додали свій GitHub:',
                    description='Зараз він виглядає так',
                    color=nextcord.Color.dark_purple())
                embed.add_field(name='Link:', value=f'**{data[7]}**', inline=False)
                embed.add_field(name=f'Repositories: ', value=f'{data[4]}')
                embed.add_field(name='Followers: ', value=f'{data[3]}')
                embed.add_field(name='Stars: ', value=f'{data[5]}')
                embed.add_field(name='Location:', value=f'{data[9]}')
                embed.add_field(name='Created at:', value=f'{data[8]}')
                embed.set_thumbnail(url=f'{data[6]}')
                embed.set_image(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
                embed.set_footer(text='GitHub Stats',
                                 icon_url='https://static-00.iconduck.com/assets.00/github-icon-2048x1988-jzvzcf2t.png')
                await interaction.send(embed=embed, ephemeral=True)
                embed = nextcord.Embed(
                    title=f'🧑‍💻 {data[2]}',
                    description=f'**GitHub** користувача <@{interaction.user.id}>',
                    color=nextcord.Color.dark_purple(), url=f'{data[7]}')
                embed.add_field(name='Link:', value=f'**{data[7]}**', inline=False)
                embed.add_field(name=f'Repositories: ', value=f'{data[4]}')
                embed.add_field(name='Followers: ', value=f'{data[3]}')
                embed.add_field(name='Stars: ', value=f'{data[5]}')
                embed.add_field(name='Location:', value=f'{data[9]}')
                embed.add_field(name='Created at:', value=f'{data[8]}')
                embed.set_thumbnail(url=f'{data[6]}')
                embed.set_image(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
                embed.set_footer(text='GitHub Stats',
                                 icon_url='https://static-00.iconduck.com/assets.00/github-icon-2048x1988-jzvzcf2t.png')
                link_button = Button(label="GitHub", style=ButtonStyle.link,
                                     url=data[7], emoji='👤')
                link_repo_button = Button(label="Repositories", style=ButtonStyle.link,
                                          url=f'https://github.com/{user_info["login"]}?tab=repositories', emoji='📗')
                my_view = View()
                my_view.add_item(link_button)
                my_view.add_item(link_repo_button)
                channel = self.bot.get_channel(1151422479303192587)
                await channel.send(embed=embed, view=my_view)
        else:
            await self.server_error(interaction)

    # slash command to see a GitHub profile
    @nextcord.slash_command(name=f'github', description=f'💙 GitHub Учасника 💛')
    async def github_profile(self, interaction: nextcord.Interaction, member: nextcord.Member = SlashOption(
        name="учасник",
        description="якщо не обраний, то побачиш свій github",
        default=None
    )):

        data = load_data()

        if member is None:

            if str(interaction.user.id) in data:
                data = data[str(interaction.user.id)]
                user_info = get_github_info(user_login=data[2])

                if user_info:
                    data = data_update(user_id=interaction.user.id, user_name=interaction.user.name, git_info=user_info)
                    data = data[str(interaction.user.id)]
                    embed = nextcord.Embed(
                        title=f'🧑‍💻 {data[2]}',
                        description=f'**GitHub** користувача <@{interaction.user.id}>',
                        color=nextcord.Color.dark_purple(), url=f'{data[7]}')
                    embed.add_field(name='Link:', value=f'**{data[7]}**', inline=False)
                    embed.add_field(name=f'Repositories: ', value=f'{data[4]}')
                    embed.add_field(name='Followers: ', value=f'{data[3]}')
                    embed.add_field(name='Stars: ', value=f'{data[5]}')
                    embed.add_field(name='Location:', value=f'{data[9]}')
                    embed.add_field(name='Created at:', value=f'{data[8]}')
                    embed.set_thumbnail(url=f'{data[6]}')
                    embed.set_image(
                        url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
                    embed.set_footer(text='GitHub Stats',
                                     icon_url='https://static-00.iconduck.com/assets.00/github-icon-2048x1988-jzvzcf2t.png')
                    link_button = Button(label="GitHub", style=ButtonStyle.link,
                                         url=data[7], emoji='👤')
                    link_repo_button = Button(label="Repositories", style=ButtonStyle.link,
                                              url=f'https://github.com/{user_info["login"]}?tab=repositories',
                                              emoji='📗')
                    my_view = View()
                    my_view.add_item(link_button)
                    my_view.add_item(link_repo_button)
                    await interaction.send(embed=embed, view=my_view, ephemeral=True)
                else:
                    await self.server_error(interaction)
            else:
                embed = nextcord.Embed(
                    title='❌ Цей користувач не додавав Github.',
                    description='Учасник не додавав GitHub до своєї сторінки на сервері.',
                    color=nextcord.Color.dark_purple())
                embed.set_image(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
                embed.set_thumbnail(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
                await interaction.send(embed=embed, ephemeral=True)
        else:
            if str(member.id) in data:
                data = data[str(member.id)]
                user_info = get_github_info(user_login=data[2])

                if user_info:
                    data = data_update(user_id=member.id, user_name=member.name, git_info=user_info)
                    data = data[str(member.id)]
                    embed = nextcord.Embed(
                        title=f'🧑‍💻 {data[2]}',
                        description=f'GitHub користувача <@{member.id}>',
                        color=nextcord.Color.dark_purple(), url=f'https://github.com/{data[2]}')
                    embed.add_field(name='Link:', value=f'{data[7]}')
                    embed.add_field(name=f'Repositories: ', value=f'{data[4]}', inline=False)
                    embed.add_field(name='Followers: ', value=f'{data[3]}', inline=False)
                    embed.add_field(name='Stars: ', value=f'{data[5]}', inline=False)
                    embed.set_image(
                        url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
                    embed.set_footer(text='GitHub Stats',
                                     icon_url='https://static-00.iconduck.com/assets.00/github-icon-2048x1988-jzvzcf2t.png')
                    link_button = Button(label="GitHub", style=ButtonStyle.link,
                                         url=data[7], emoji='👤')
                    link_repo_button = Button(label="Repositories", style=ButtonStyle.link,
                                              url=f'https://github.com/{user_info["login"]}?tab=repositories',
                                              emoji='📗')
                    my_view = View()
                    my_view.add_item(link_button)
                    my_view.add_item(link_repo_button)
                    await interaction.send(embed=embed, view=my_view, ephemeral=True)
                else:
                    await self.server_error(interaction)
            else:
                embed = nextcord.Embed(
                    title='❌ Цей користувач не додавав Github.',
                    description='Учасник не додавав GitHub до своєї сторінки на сервері.',
                    color=nextcord.Color.dark_purple())
                embed.set_image(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
                embed.set_thumbnail(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
                await interaction.send(embed=embed, ephemeral=True)

    # slash command for update info about GitHub profile
    @nextcord.slash_command(name=f'gitupdate', description=f'💙 Оновити свій GitHub 💛')
    @cooldowns.cooldown(1, 259200, bucket=cooldowns.SlashBucket.author)
    async def github_profile_update(self, interaction: nextcord.Interaction):
        data = load_data()

        if str(interaction.user.id) in data:
            data = data[str(interaction.user.id)]
            user_info = get_github_info(user_login=data[2])

            if user_info:
                data = data_update(user_id=interaction.user.id, user_name=interaction.user.name, git_info=user_info)
                data = data[str(interaction.user.id)]
                embed = nextcord.Embed(
                    title=f'🧑‍💻 {data[2]}',
                    description=f'Ви успішно оновили свій GitHub в каналі:  <#1151422479303192587>',
                    color=nextcord.Color.dark_purple(), url=f'{data[7]}')
                embed.add_field(name='Наступне оновлення доступне через:', value='**3 Дні.**')
                embed.add_field(name='Link:', value=f'**{data[7]}**', inline=False)
                embed.add_field(name=f'Repositories: ', value=f'{data[4]}')
                embed.add_field(name='Followers: ', value=f'{data[3]}')
                embed.add_field(name='Stars: ', value=f'{data[5]}')
                embed.add_field(name='Location:', value=f'{data[9]}')
                embed.add_field(name='Created at:', value=f'{data[8]}')
                embed.set_thumbnail(url=f'{data[6]}')
                embed.set_image(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
                embed.set_footer(text='GitHub Stats',
                                 icon_url='https://static-00.iconduck.com/assets.00/github-icon-2048x1988-jzvzcf2t.png')
                link_button = Button(label="GitHub", style=ButtonStyle.link,
                                     url=data[7], emoji='👤')
                link_repo_button = Button(label="Repositories", style=ButtonStyle.link,
                                          url=f'https://github.com/{user_info["login"]}?tab=repositories', emoji='📗')
                my_view = View()
                my_view.add_item(link_button)
                my_view.add_item(link_repo_button)
                await interaction.send(embed=embed, view=my_view, ephemeral=True)
                embed = nextcord.Embed(
                    title=f'🧑‍💻 {data[2]}',
                    description=f'**GitHub** користувача <@{interaction.user.id}>',
                    color=nextcord.Color.dark_purple(), url=f'{data[7]}')
                embed.add_field(name='Link:', value=f'**{data[7]}**', inline=False)
                embed.add_field(name=f'Repositories: ', value=f'{data[4]}')
                embed.add_field(name='Followers: ', value=f'{data[3]}')
                embed.add_field(name='Stars: ', value=f'{data[5]}')
                embed.add_field(name='Location:', value=f'{data[9]}')
                embed.add_field(name='Created at:', value=f'{data[8]}')
                embed.set_thumbnail(url=f'{data[6]}')
                embed.set_image(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
                embed.set_footer(text='GitHub Stats',
                                 icon_url='https://static-00.iconduck.com/assets.00/github-icon-2048x1988-jzvzcf2t.png')
                link_button = Button(label="GitHub", style=ButtonStyle.link,
                                     url=data[7], emoji='👤')
                link_repo_button = Button(label="Repositories", style=ButtonStyle.link,
                                          url=f'https://github.com/{user_info["login"]}?tab=repositories', emoji='📗')
                my_view = View()
                my_view.add_item(link_button)
                my_view.add_item(link_repo_button)
                channel = self.bot.get_channel(1151422479303192587)
                await channel.send(embed=embed, view=my_view)
            else:
                await self.server_error(interaction)
        else:
            embed = nextcord.Embed(
                title='❌ Ти не додавав Github.',
                description='Ви не додавали GitHub до своєї сторінки на сервері.',
                color=nextcord.Color.dark_purple())
            embed.add_field(name='Команда щоб додати:', value='`/gitprofile`')
            embed.set_image(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)

    # slash command to delite a GitHub profile
    @nextcord.slash_command(name=f'gitdel', description=f'💙 Видалити свій GitHub 💛')
    async def github_profile_del(self, interaction: nextcord.Interaction):
        data = load_data()

        if str(interaction.user.id) in data:
            embed = nextcord.Embed(
                title='👀 Ви впевнені?',
                description="Ви дійсно хочете відв'язати світ **GitHub**?",
                color=nextcord.Color.dark_purple())
            embed.set_image(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            view = GitDel()
            await interaction.send(embed=embed, ephemeral=True, view=view, delete_after=60)
            await view.wait()
            if view.value is None:
                return
            elif view.value:
                del data[str(interaction.user.id)]

                save_data(data)
                embed = nextcord.Embed(
                    title='✅ Ви успішно видалили свій GitHub',
                    description='Щоб знову додати **GitHub** скористайтеся командою: `/gitprofile`',
                    color=nextcord.Color.dark_purple())
                embed.set_image(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
                embed.set_thumbnail(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
                await interaction.send(embed=embed, ephemeral=True)
            else:
                data = data[str(interaction.user.id)]
                embed = nextcord.Embed(
                    title=f'🧑‍💻 {data[2]}',
                    description=f'**GitHub** користувача <@{interaction.user.id}>',
                    color=nextcord.Color.dark_purple(), url=f'{data[7]}')
                embed.add_field(name='Link:', value=f'**{data[7]}**', inline=False)
                embed.add_field(name=f'Repositories: ', value=f'{data[4]}')
                embed.add_field(name='Followers: ', value=f'{data[3]}')
                embed.add_field(name='Stars: ', value=f'{data[5]}')
                embed.add_field(name='Location:', value=f'{data[9]}')
                embed.add_field(name='Created at:', value=f'{data[8]}')
                embed.set_thumbnail(url=f'{data[6]}')
                embed.set_image(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694586847/github_card_pjwvvp.png')
                embed.set_footer(text='GitHub Stats',
                                 icon_url='https://static-00.iconduck.com/assets.00/github-icon-2048x1988-jzvzcf2t.png')
                link_button = Button(label="GitHub", style=ButtonStyle.link,
                                     url=data[7], emoji='👤')
                link_repo_button = Button(label="Repositories", style=ButtonStyle.link,
                                          url=f'https://github.com/{data[2]}?tab=repositories', emoji='📗')
                my_view = View()
                my_view.add_item(link_button)
                my_view.add_item(link_repo_button)
                await interaction.send(embed=embed, view=my_view, ephemeral=True)
        else:
            embed = nextcord.Embed(
                title='❌ Ти не додавав Github.',
                description='Ви не додавали GitHub до своєї сторінки на сервері.',
                color=nextcord.Color.dark_purple())
            embed.add_field(name='Команда щоб додати:', value='`/gitprofile`')
            embed.set_image(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)


# function to register the GitHub user cog with the bot
def register_github_cogs(bot: Bot) -> None:
    bot.add_cog(__GitHubUserCog(bot))
