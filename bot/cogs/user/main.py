import random

import aiohttp
import nextcord
import openai
import pyshorteners as pyshorteners
import replicate
import requests
import translators as ts
from nextcord import SlashOption, ButtonStyle
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
    async def tag(self, interaction: nextcord.Interaction, user: nextcord.Member):
        embed = nextcord.Embed(title='🔔 Учасник',
                               description=f'**{user.mention}, тебе гукає гайдамака: {interaction.user.mention}**',
                               colour=nextcord.Color.red())
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, delete_after=900)
        await user.send(embed=embed, delete_after=900)

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
            color=nextcord.Color.red()
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
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed, ephemeral=True, delete_after=60)

    # Randomly
    @nextcord.slash_command(name=f'random', description=f'💙 Випадкове число 💛')
    async def roll(self, interaction: nextcord.Interaction, snum: int = SlashOption(
        name="діапазоном",
        description="до числа:",
        default=None
    )):
        if snum == None:
            embed = nextcord.Embed(title='🎲 Випадкове число:', description=f"**{(random.randint(1, 101))}**",
                                   color=nextcord.Color.purple())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.send(embed=embed, delete_after=100)
        else:
            embed = nextcord.Embed(title='🎲 Випадкове число:', description=f"**{(random.randint(1, int(snum)))}**",
                                   color=nextcord.Color.purple())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.send(embed=embed, delete_after=30)

    # Coin
    @nextcord.slash_command(name=f'coin', description=f'💙 Підкинь монетку 💛')
    async def coin(self, interaction: nextcord.Interaction):
        variants = ['Орел', 'Решка']
        coin = random.choice(variants)
        embed = nextcord.Embed(title='🪙 Випала сторона монети:', description=f"**{coin}**",
                               colour=nextcord.Color.purple())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        if coin == 'Орел':
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/1016748092810346507/1053567689689407528/1.png')
        else:
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/1016748092810346507/1053567595548258404/9f4b6da930092858.png')
        await interaction.send(embed=embed, delete_after=30)

    # mems
    @nextcord.slash_command(name=f'meme', description=f'💙 Прикольчік 💛')
    async def meme(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="", description="", colour=nextcord.Color.purple())

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
                await interaction.send(embed=embed)

    # weathering
    @nextcord.slash_command(name=f'weather', description=f'💙 Прогноз погоди 💛')
    async def weather(self, interaction: nextcord.Interaction, city: str = None):
        if city == None:
            embed = nextcord.Embed(title=":x:Трясся твоїй матері! Вкажи місто!",
                                   description='Ви не вказали місто, де хочете дізнатися погоду.',
                                   colour=nextcord.Color.red())
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
                                           color=nextcord.Color.red())
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
                                       colour=nextcord.Color.red())
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
        # Выводим первый результат поиска
        if "items" in data:
            embed = nextcord.Embed(title='Результати пошуку:', colour=nextcord.Color.red())
            for i in range(5):
                item = data["items"][i]
                title = item["title"]
                link = item["link"]
                embed.add_field(name=title, value=link, inline=False)

            embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/1016748092810346507/1062107301839904768/Google-G-Logo-PNG-Image.png?width=671&height=671")
            await interaction.send(embed=embed, delete_after=60)
        else:
            await interaction.send("Ничего не найдено.")

    # imagine
    #@nextcord.slash_command(name=f'imagine', description=f'💙 Генерація зображення 💛')
    @commands.has_role(1008805712715055104 or 1010216550927699969)
    async def imagine(self, interaction: nextcord.Interaction, params=SlashOption(
        name="параметри",
        description="чим більше ви опишите, тим краще буде результат. на англійській мові результат буде більш точним"
    )):
        roles = interaction.user.roles
        if nextcord.utils.get(roles, name="imaginete"):
            embed = nextcord.Embed(title=f"🖼 Треба трошки почекати. 🕑",
                                   description=f'{interaction.user.mention}, Система генерує ваше зображення.',
                                   colour=nextcord.Color.red())
            embed.set_image(url="https://rb.ru/media/upload_tmp/2018/d3.gif")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed1 = nextcord.Embed(title=f"🖼 Треба трошки почекати.. 🕑",
                                    description=f'{interaction.user.mention}, Система генерує ваше зображення.',
                                    colour=nextcord.Color.red())
            embed1.set_image(url="https://rb.ru/media/upload_tmp/2018/d3.gif")
            embed1.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed2 = nextcord.Embed(title=f"🖼 Треба трошки почекати... 🕑",
                                    description=f'{interaction.user.mention}, Система генерує ваше зображення.',
                                    colour=nextcord.Color.red())
            embed2.set_image(url="https://rb.ru/media/upload_tmp/2018/d3.gif")
            embed2.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            msg = await interaction.send(embed=embed)
            await msg.edit(embed=embed1)
            await msg.edit(embed=embed2)
            model = replicate.models.get("tstramer/midjourney-diffusion")
            version = model.versions.get("436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b")
            image = version.predict(prompt=params, num_inference_steps=75)[0]
            embed = nextcord.Embed(title=f"🖼️ Ось, що в нас вийшло:",
                                   description=f'Для кращого результату введіть більше інформації. {interaction.user.mention}',
                                   colour=nextcord.Color.red())
            embed.set_image(url=image)
            download_button = Button(label="Завантажити", style=ButtonStyle.blurple, url=image)
            my_view = View(timeout=180)
            my_view.add_item(download_button)
            await msg.edit(embed=embed, view=my_view, delete_after=1)
            await interaction.send(embed=embed, view=my_view)
        else:
            embed = nextcord.Embed(title=f"❗Ти не маєш доступу❗",
                                   description=f'Для того щоб отримати доступ до команди, напишіть до адміністрації <@872455283560042526>. Вибачте за незручності, {interaction.user.mention}',
                                   colour=nextcord.Color.red())
            embed.set_image(url="https://i.gifer.com/origin/3a/3ad09d4905511990cccc98d904bd1e94.gif")
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.send(embed=embed)

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
                               colour=nextcord.Color.red())
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.send(embed=embed, delete_after=60)

    #@nextcord.slash_command(name=f'gpt', description=f'💙 Використайте можливості ChatCPT 💛')
    @commands.has_role(1008805712715055104 or 1010216550927699969)
    async def gpt(self, interaction: nextcord.Interaction, prompt=SlashOption(
        name="запит",
        description="чим більше ви опишите, тим краще буде результат. на англійській мові результат буде більш точним"
    )):
        msg = await interaction.send('🕑 Треба трошки почекати... Генеруємо відповідь🚀')
        await msg.edit('🕑 Треба трошки почекати. Генеруємо відповідь🚀')
        await msg.edit('🕑 Треба трошки почекати.. Генеруємо відповідь🚀')
        my_set = {prompt,}
        my_list = list(my_set)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "assistant", "content": f"{prompt}"},]).get("choices")[0].message
        await msg.edit(response)

        # lexica
        @nextcord.slash_command(name=f'lexica', description=f'💙 Велетенська база вже згенерованих зображень 💛')
        @commands.has_role(1008805712715055104 or 1010216550927699969)
        async def lexica(self, interaction: nextcord.Interaction, params=SlashOption(
            name="параметри",
            description="чим більше ви опишите, тим краще буде результат. на англійській мові результат буде більш точним"
        )):
            roles = interaction.user.roles
            if nextcord.utils.get(roles, name="imaginete"):
                url = f'https://lexica.art/api/v1/search?q={params}'
                response = requests.get(url)
                data = response.json()
                src = data['images'][0].get('gallery')
                embed = nextcord.Embed(title=f"🖼️ Ось, що ми знайшли:",
                                       description=f'Для кращого результату введіть більше інформації. {interaction.user.mention}',
                                       colour=nextcord.Color.red(),
                                       url=src)
                embed.set_image(url="https://lexica.art/lexica-meta.png")
                download_button = Button(label="Відкрити колекцію", style=ButtonStyle.blurple, url=src)
                my_view = View(timeout=180)
                my_view.add_item(download_button)
                await interaction.send(embed=embed, view=my_view)
            else:
                embed = nextcord.Embed(title=f"❗Ти не маєш доступу❗",
                                       description=f'Для того щоб отримати доступ до команди, напишіть до адміністрації <@872455283560042526>. Вибачте за незручності, {interaction.user.mention}',
                                       colour=nextcord.Color.red())
                embed.set_image(url="https://i.gifer.com/origin/3a/3ad09d4905511990cccc98d904bd1e94.gif")
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await interaction.send(embed=embed)

        # upscale
       # @nextcord.slash_command(name=f'upscale', description=f'💙 Збільшити зображення без втрати якості 💛')
        @commands.has_role(1008805712715055104 or 1010216550927699969)
        async def upscale(self, interaction: nextcord.Interaction, url=SlashOption(
            name="посилання",
            description="на ваше зображення"
        )):
            roles = interaction.user.roles
            if nextcord.utils.get(roles, name="imaginete"):
                embed = nextcord.Embed(title=f"🖼 Треба трошки почекати... 🕑",
                                       description=f'{interaction.user.mention}, Система генерує ваше зображення.',
                                       colour=nextcord.Color.red())
                embed.set_image(url="https://rb.ru/media/upload_tmp/2018/d3.gif")
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                msg = await interaction.send(embed=embed)
                r = requests.post(
                    "https://api.deepai.org/api/waifu2x",
                    data={
                        'image': f'{url}',
                    },
                    headers={'api-key': 'ec5d28fe-7a02-4004-90b0-4848465e7740'}
                )
                r = r.json()
                image = r["output_url"]
                embed = nextcord.Embed(title=f"🖼️ Ось, що в нас вийшла:",
                                       description=f'Ми збільшили ваше зображення. {interaction.user.mention}',
                                       colour=nextcord.Color.red(),
                                       url=image)
                embed.set_image(url=image)
                download_button = Button(label="Завантажити", style=ButtonStyle.blurple, url=image)
                my_view = View(timeout=180)
                my_view.add_item(download_button)
                await msg.edit(embed=embed, view=my_view)
            else:
                embed = nextcord.Embed(title=f"❗Ти не маєш доступу❗",
                                       description=f'Для того щоб отримати доступ до команди, напишіть до адміністрації <@872455283560042526>. Вибачте за незручності, {interaction.user.mention}',
                                       colour=nextcord.Color.red())
                embed.set_image(url="https://i.gifer.com/origin/3a/3ad09d4905511990cccc98d904bd1e94.gif")
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await interaction.send(embed=embed)

def register_user_cogs(bot: Bot) -> None:
    bot.add_cog(__MainUserCog(bot))
