import random
from typing import Optional
from cooldowns import SlashBucket, CallableOnCooldown
import cooldowns
import aiohttp
import nextcord
import openai
import pyshorteners as pyshorteners
import replicate
import requests
import translators as ts
from cooldowns import CooldownBucketProtocol
from cooldowns.utils import MaybeCoro
from easy_pil import Editor, Font
from nextcord import SlashOption, ButtonStyle, File
from nextcord.ext import commands
from nextcord.ext.commands import Cog, Bot
from nextcord.ui import Button, View


# todo: UserCogs


class __MainUserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    openai.api_key = "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"

    # Mention user
    @nextcord.slash_command(name=f'tag', description=f'💙 Відмітити учасника 💛')
    @cooldowns.cooldown(1, 3600, bucket=cooldowns.SlashBucket.author)
    async def tag(self, interaction: nextcord.Interaction, user: nextcord.Member):
        embed = nextcord.Embed(title='🔔 Учасник',
                               description=f'**{user.mention}, тебе гукає гайдамака: {interaction.user.mention}**',
                               colour=nextcord.Color.dark_purple())
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, delete_after=300)
        await user.send(embed=embed, delete_after=300)

    # Show avatar
    @nextcord.slash_command(name=f'avatar', description=f'💙 Побачити аватар користувача або свій 💛')
    async def avatar(self, interaction: nextcord.Interaction, member: nextcord.Member = SlashOption(
        name="учасник",
        description="якщо не обраний, то побачиш свій аватар",
        default=None
    )):
        if member == None:
            download_button = Button(label="Завантажити", style=ButtonStyle.blurple, url=interaction.user.avatar.url)
            embed = nextcord.Embed(title="🔗 Завантажити", url=interaction.user.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_image(url=interaction.user.avatar.url)
            embed.set_footer(text=f'Аватар користувача: {interaction.user.name}.')
            my_view = View(timeout=180)
            my_view.add_item(download_button)
            await interaction.response.send_message(embed=embed, view=my_view, delete_after=200)
        else:
            download_button = Button(label="Завантажити", style=ButtonStyle.blurple, url=member.avatar.url)
            embed = nextcord.Embed(title="🔗 Завантажити", url=member.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_image(url=member.avatar.url)
            embed.set_footer(text=f'Аватар користувача: {member.name}.')
            my_view = View(timeout=180)
            my_view.add_item(download_button)
            await interaction.response.send_message(embed=embed, view=my_view, delete_after=200)

    # Show server avatar
    @nextcord.slash_command(name=f'serverava', description=f'💙 Побачити аватар серверу 💛')
    async def avaserver(self, interaction: nextcord.Interaction):
        download_button = Button(label="Завантажити", style=ButtonStyle.blurple, url=interaction.guild.icon.url)
        embed = nextcord.Embed(title="🔗 Завантажити", url=interaction.guild.icon.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_image(url=interaction.guild.icon.url)
        embed.set_footer(text=f'Аватар сервера: {interaction.guild.name}.')
        my_view = View(timeout=180)
        my_view.add_item(download_button)
        await interaction.send(embed=embed, view=my_view, ephemeral=True, delete_after=200)

    # Server Info
    @nextcord.slash_command(name=f'server', description=f'💙 Інформація про сервер 💛')
    async def server(self, interaction: nextcord.Interaction):
        format = "**%d** %b | %Y "
        name = interaction.guild.name
        description = str(interaction.guild.description)
        role_count = len(interaction.guild.roles)
        id = str(interaction.guild.id)
        memberCount = str(interaction.guild.member_count)
        text_channels = len(interaction.guild.text_channels)
        voice_channels = len(interaction.guild.voice_channels)
        channels = text_channels + voice_channels
        icon = str(interaction.guild.icon.url)
        embed = nextcord.Embed(
            title=name,
            color=nextcord.Color.dark_purple()
        )
        embed.set_thumbnail(url=icon)
        embed.set_author(name="Інформація про сервер: ", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=":id: Server ID", value=id, inline=True)
        embed.add_field(name=":clock1: Створений", value=f"{interaction.guild.created_at.strftime(format)}",
                        inline=True)
        embed.add_field(name=f":closed_lock_with_key: Ролі", value=f"**{role_count}** Ролей")
        embed.add_field(name=f":busts_in_silhouette: Учасники ({memberCount})", value=f"**{memberCount}** Учасників",
                        inline=True)
        embed.add_field(name=f":speech_balloon: Канали ({channels})",
                        value=f"**{text_channels}** Текстові| **{voice_channels}** Голосові")
        embed.add_field(name="🍼 Створений", value="by <@872455283560042526>")
        embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694447835/information_hevmub.png')
        await interaction.send(embed=embed, ephemeral=True, delete_after=60)

    # Randomly
    @nextcord.slash_command(name=f'random', description=f'💙 Випадкове число 💛')
    async def roll(self, interaction: nextcord.Interaction):
        background = Editor(f"randomly.png")
        poppins = Font.montserrat(size=180, variant='bold')
        text_color = "#ffffff"
        num = random.randint(1, 101)
        background.text((1265, 130), str(num), font=poppins, color=text_color, align='center')
        card = File(fp=background.image_bytes, filename="level.png")
        await interaction.send(file=card, content=f'**🎲 Випадкове число:** **{num}**', ephemeral=True, delete_after=60)

    # Coin
    @nextcord.slash_command(name=f'coin', description=f'💙 Підкинь монетку 💛')
    async def coin(self, interaction: nextcord.Interaction):
        variants = ['Орел', 'Решка']
        coin = random.choice(variants)
        embed = nextcord.Embed(title='🪙 Випала сторона монети:', description='',
                               colour=nextcord.Color.dark_purple())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        if coin == 'Орел':
            embed.set_image(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694448259/%D0%BE%D1%80%D0%B5%D0%BB_nzxqfl.png')
        else:
            embed.set_image(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694448180/%D1%80%D0%B5%D1%88%D0%BA%D0%B0_y23xps.png')
        await interaction.send(embed=embed, delete_after=30)

    # mems
    @nextcord.slash_command(name=f'meme', description=f'💙 Прикольчік 💛')
    async def meme(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="", description="", colour=nextcord.Color.dark_purple())

        async with aiohttp.ClientSession() as cs:
            URL = ['https://www.reddit.com/r/RussiaUkraineWarMemes/new.json?sort=hot',
                   'https://www.reddit.com/r/ukrainememes/new.json?sort=hot',
                   'https://www.reddit.com/r/uamemesforces/new.json?sort=hot',
                   'https://www.reddit.com/r/ukraine22memes/new.json?sort=hot',
                   'https://www.reddit.com/r/UkrainianMemes/new.json?sort=hot',
                   'https://www.reddit.com/r/Ukraine_in_memes/new.json?sort=hot',
                   'https://www.reddit.com/r/dankmemes/new.json?sort=hot']
            async with cs.get(random.choice(URL)) as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await interaction.send(embed=embed, delete_after=120)

    # weathering
    @nextcord.slash_command(name=f'weather', description=f'💙 Прогноз погоди 💛')
    async def weather(self, interaction: nextcord.Interaction, city: str = None):
        if city == None:
            embed = nextcord.Embed(title=":x:Трясся твоїй матері! Вкажи місто!",
                                   description='Ви не вказали місто, де хочете дізнатися погоду.',
                                   colour=nextcord.Color.dark_purple())
            embed.add_field(name='Правильний вигляд команди:', value='```/weather citi```', inline=False)
            embed.add_field(name='Назву міста можно писати:', value='```на Українській та москальській мові.```',
                            inline=False)
            embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True, delete_after=60)
        else:
            api_key = "f2954a7666f59b7c9b62f994ad7298b6"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            city_name = city
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            channel = interaction.channel
            if x["cod"] != "404":
                async with channel.typing():
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_temperature_celsiuis = str(round(current_temperature - 273.15))
                    current_pressure = y["pressure"]
                    current_humidity = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    ts_weather_description = ts.google(weather_description, translator=ts.google, to_language='uk')
                    eather_description = z[0]["description"]
                    embed = nextcord.Embed(title=f"🌈 Погода в {city_name}",
                                           color=nextcord.Color.dark_purple())
                    embed.add_field(name="⛅ Опис:", value=f"**{ts_weather_description}**", inline=False)
                    embed.add_field(name="🌡 Температура(C):", value=f"**{current_temperature_celsiuis}°C**",
                                    inline=False)
                    embed.add_field(name="💧 Вологість повітря(%):", value=f"**{current_humidity}%**", inline=False)
                    embed.add_field(name="🗜 Атмосферний тиск(hPa):", value=f"**{current_pressure}hPa**", inline=False)
                    embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                    embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
                    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                    await channel.send(embed=embed, delete_after=60)
            else:
                embed = nextcord.Embed(title=":x:Трясся твоїй матері! Вкажи правильне місто!",
                                       description='Ви не правильно вказали місто, де хочете дізнатися погоду.',
                                       colour=nextcord.Color.dark_purple())
                embed.add_field(name='Правильний вигляд команди:', value='```.weather citi```', inline=False)
                embed.add_field(name='Назву міста можно писати:', value='```на Українській та москальській мові.```',
                                inline=False)
                embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await interaction.send(embed=embed, ephemeral=True, delete_after=60)

    # google
    @nextcord.slash_command(name=f'googlе', description=f'💙 Прогуглити 💛')
    async def googlе(self, interaction: nextcord.Interaction, query):
        api_key = "AIzaSyApJI_7WlmSuoWq4idbfD98x-pIsh0tJ6Q"
        cx = "95e537e092f254d28"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
        r = requests.get(url)
        data = r.json()
        # Output the first search result
        if "items" in data:
            embed = nextcord.Embed(title='Результати пошуку:', colour=nextcord.Color.dark_purple())
            for i in range(5):
                item = data["items"][i]
                title = item["title"]
                link = item["link"]
                embed.add_field(name=title, value=link, inline=False)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/1016748092810346507/1062107301839904768/Google-G-Logo-PNG-Image.png?width=671&height=671")
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694448536/google_card_fcsiqb.png')
            await interaction.send(embed=embed, ephemeral=True, delete_after=60)
        else:
            embed = nextcord.Embed(title='Нічого не знайдено🤷‍♂️', colour=nextcord.Color.dark_purple())
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            await interaction.send(embed=embed, ephemeral=True, delete_after=60)

    # Short your link
    @nextcord.slash_command(name=f'short', description=f'💙 Скоротити посилання 💛')
    async def short(self, interaction: nextcord.Interaction, url=SlashOption(
        name="параметри",
        description="чим більше ви опишите, тим краще буде результат. на англійській мові результат буде більш точним"
    )):
        url = url
        s = pyshorteners.Shortener()
        shorturl = s.tinyurl.short(url)
        embed = nextcord.Embed(title='🔗 Ось ваше посилання:', description=f"Link: {shorturl}",
                               colour=nextcord.Color.dark_purple())
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.send(embed=embed, delete_after=60)


def register_user_cogs(bot: Bot) -> None:
    bot.add_cog(__MainUserCog(bot))
