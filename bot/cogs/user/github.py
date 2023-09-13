import json

import cooldowns
import nextcord
import requests
from nextcord import SlashOption, ButtonStyle
from nextcord.ext.commands import Bot
from nextcord.ext.commands import Cog
from nextcord.ui import Button, View


# todo: GitHubCogs


class GitDel(nextcord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Видалити", style=nextcord.ButtonStyle.green, emoji='🗑')
    async def profile_del(self, buttun: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()
    @nextcord.ui.button(label="Відмінити", style=nextcord.ButtonStyle.red, emoji='✖')
    async def profile_del_cansel(self, buttun: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()

class __GitHubUserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name=f'gitprofile', description=f'💙 Додати свій профіль GitHub 💛')
    async def github_add_profile(self, interaction: nextcord.Interaction, username=SlashOption(
        name="нікнейм",
        description="встав сюди свій github нікнейм")):

        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        if response.status_code == 200:
            user_info = response.json()
            login = user_info['login']
            file_name = "github_users.json"
            try:
                # Load current data from the file (if available)
                with open(file_name, 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                # If no file is found, create an empty dictionary
                data = {}

            if str(interaction.user.id) in data:
                data[str(interaction.user.id)] = interaction.user.name, interaction.user.id, login, user_info[
                    'followers'], user_info['public_repos'], user_info['starred_url'].count('{/repo}'), user_info[
                    'avatar_url'], user_info['html_url'], user_info['created_at'][:10], user_info['location']
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)
                with open(file_name, 'r') as file:
                    data = json.load(file)
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
                data[interaction.user.id] = interaction.user.name, interaction.user.id, login, user_info[
                    'followers'], user_info['public_repos'], user_info['starred_url'].count('{/repo}'), user_info[
                    'avatar_url'], user_info['html_url'], user_info['created_at'][:10], user_info['location']

                # Записываем обновленные данные в файл
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)
                with open(file_name, 'r') as file:
                    data = json.load(file)
                embed = nextcord.Embed(
                    title='✅ Ви успішно додали свій GitHub:',
                    description='Зараз він виглядає так',
                    color=nextcord.Color.dark_purple())
                data = data[str(interaction.user.id)]
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
                                          url=f'https://github.com/{login}?tab=repositories', emoji='📗')
                my_view = View()
                my_view.add_item(link_button)
                my_view.add_item(link_repo_button)
                channel = self.bot.get_channel(1151422479303192587)
                await channel.send(embed=embed, view=my_view)
        else:
            embed = nextcord.Embed(
                title='❌ Помилка на стороні серверу!',
                description='Не вдалося додати ваш профіль GitHub. Спробуйте пізніше, або зверніться до адміністрації.',
                color=nextcord.Color.dark_purple())
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(name=f'github', description=f'💙 GitHub Учасника 💛')
    async def github_profile(self, interaction: nextcord.Interaction, member: nextcord.Member = SlashOption(
        name="учасник",
        description="якщо не обраний, то побачиш свій github",
        default=None
    )):

        file_name = "github_users.json"
        try:
            # Load current data from the file (if available)
            with open(file_name, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If no file is found, create an empty dictionary
            data = {}

        if member == None:
            if str(interaction.user.id) in data:
                url = f"https://api.github.com/users/{data[str(interaction.user.id)][2]}"
                response = requests.get(url)
                if response.status_code == 200:
                    user_info = response.json()
                    login = user_info['login']
                    data[str(interaction.user.id)] = interaction.user.name, interaction.user.id, login, user_info[
                        'followers'], user_info['public_repos'], user_info['starred_url'].count('{/repo}'), user_info[
                        'avatar_url'], user_info['html_url'], user_info['created_at'][:10], user_info['location']
                    with open(file_name, 'w') as file:
                        json.dump(data, file, indent=4)
                    with open(file_name, 'r') as file:
                        data = json.load(file)
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
                                              url=f'https://github.com/{login}?tab=repositories', emoji='📗')
                    my_view = View()
                    my_view.add_item(link_button)
                    my_view.add_item(link_repo_button)
                    await interaction.send(embed=embed, view=my_view, ephemeral=True)
                else:
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
                url = f"https://api.github.com/users/{data[str(member.id)][2]}"
                response = requests.get(url)
                if response.status_code == 200:
                    user_info = response.json()
                    login = user_info['login']
                    data[str(member.id)] = member.name, member.id, login, user_info[
                        'followers'], user_info['public_repos'], user_info['starred_url'].count('{/repo}'), user_info[
                        'avatar_url'], user_info['html_url'], user_info['created_at'][:10], user_info['location']
                    with open(file_name, 'w') as file:
                        json.dump(data, file, indent=4)
                    with open(file_name, 'r') as file:
                        data = json.load(file)
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
                                              url=f'https://github.com/{login}?tab=repositories', emoji='📗')
                    my_view = View()
                    my_view.add_item(link_button)
                    my_view.add_item(link_repo_button)
                    await interaction.send(embed=embed, view=my_view, ephemeral=True)
                else:
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

    @nextcord.slash_command(name=f'gitupdate', description=f'💙 Оновити свій GitHub 💛')
    @cooldowns.cooldown(1, 259200, bucket=cooldowns.SlashBucket.author)
    async def github_profile_update(self, interaction: nextcord.Interaction):
        file_name = "github_users.json"
        try:
            # Load current data from the file (if available)
            with open(file_name, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If no file is found, create an empty dictionary
            data = {}

        if str(interaction.user.id) in data:
            url = f"https://api.github.com/users/{data[str(interaction.user.id)][2]}"
            response = requests.get(url)
            if response.status_code == 200:
                user_info = response.json()
                login = user_info['login']
                data[str(interaction.user.id)] = interaction.user.name, interaction.user.id, login, user_info[
                    'followers'], user_info['public_repos'], user_info['starred_url'].count('{/repo}'), user_info[
                    'avatar_url'], user_info['html_url'], user_info['created_at'][:10], user_info['location']
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)
                with open(file_name, 'r') as file:
                    data = json.load(file)
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
                                          url=f'https://github.com/{login}?tab=repositories', emoji='📗')
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
                                          url=f'https://github.com/{login}?tab=repositories', emoji='📗')
                my_view = View()
                my_view.add_item(link_button)
                my_view.add_item(link_repo_button)
                channel = self.bot.get_channel(1151422479303192587)
                await channel.send(embed=embed, view=my_view)
            else:
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

    @nextcord.slash_command(name=f'gitdel', description=f'💙 Видалити свій GitHub 💛')
    async def github_profile_del(self, interaction: nextcord.Interaction):
        file_name = "github_users.json"
        try:
            # Load current data from the file (if available)
            with open(file_name, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If no file is found, create an empty dictionary
            data = {}

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

                # Write the updated data to a file
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)
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

def register_github_cogs(bot: Bot) -> None:
    bot.add_cog(__GitHubUserCog(bot))
