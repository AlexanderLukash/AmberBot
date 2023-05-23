import nextcord
import requests
from nextcord import client
from nextcord.ext import tasks
from nextcord.ext.commands import Bot, Cog
import translators as ts


# todo: OtherCogs
class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @tasks.loop(seconds=432000)
    async def check_epic_games(self):
        print("Скидки запущені")
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
        response = requests.get(url)
        data = response.json()
        for game in data["data"]["Catalog"]["searchStore"]["elements"]:
            if game["promotions"] and game["promotions"]["promotionalOffers"]:
                if not game["promotions"]["promotionalOffers"][0].get("discountSetting", {}).get("discountPercentage"):
                    game_description = game['description']
                    description = ts.google(game_description, translator=ts.google, to_language='uk')
                    embed = nextcord.Embed(title=f"{game['title']}",
                                           description=f"**{description}**",
                                           colour=nextcord.Color.red(),
                                           url=f"https://www.epicgames.com/store/en-US/p/{game['catalogNs']['mappings'][0].get('pageSlug')}")
                    embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                    embed.set_thumbnail(
                        url='https://cdn2.unrealengine.com/Unreal+Engine%2Feg-logo-filled-1255x1272-0eb9d144a0f981d1cbaaa1eb957de7a3207b31bb.png')
                    embed.set_image(url=game['keyImages'][0]['url'])
                    embed.add_field(name='**Нова роздача від Epic Games!**',
                                    value='**Не забудь забрати її собі в колекцію 💙💛**')
                    await self.bot.get_channel(1003933282267828306).send(embed=embed)


    def get_sale_data(self):
        url = 'https://store.steampowered.com/api/featuredcategories/?1&specials=1&format=json'
        response = requests.get(url)
        data = response.json()
        cat_specials = data['specials']
        items = cat_specials["items"]
        return items

    @tasks.loop(seconds=604800)
    async def check_for_new_sales(self):
        sales_data = self.get_sale_data()
        new_sales_data = [game for game in sales_data if game['discount_percent'] > 0]
        if new_sales_data:
            await self.check_steam_games(new_sales_data)


    async def check_steam_games(self, new_sales_data):
        print("Скидки стім запущені")
        embed = nextcord.Embed(title=f"Нові знишки Steam",
                               description=f"**Рекомендовані:**",
                               colour=nextcord.Color.red(),
                               url=f"https://store.steampowered.com/search/?specials=1")
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(
            url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/800px-Steam_icon_logo.svg.png')
        embed.set_image(url="https://pictures.ua.tribuna.com/image/6947c6cd-1c7f-462e-83da-502978fb7c11")
        for game in new_sales_data:
            embed.add_field(name=f'**{game["name"]}**',
                            value=f'**Знишка: {game["discount_percent"]}%, Ціна: ~~ {str(game["original_price"])[:-2]} ~~   {str(game["final_price"])[:-2]} USD**', inline=False)
        embed.add_field(name='**Нові скидки від Steam!**',
                        value='**Встигни зекономити 💙💛**', inline=False)
        await self.bot.get_channel(1003933282267828306).send(embed=embed)







    @Cog.listener()
    async def on_ready(self) -> None:
        print("Бот прокинувся та готовий до роботи!")
        await self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game('/help'))
        self.check_epic_games.start()
        self.check_for_new_sales.start()

def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
