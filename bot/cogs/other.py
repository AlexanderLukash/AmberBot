import nextcord
from nextcord.ext.commands import Bot, Cog




# todo: OtherCogs


class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        print("Бот прокинувся та готовий до роботи!")
        await self.bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game('/help'))



def register_other_cogs(bot: Bot) -> None:
    bot.add_cog(__MainOtherCog(bot))
