import datetime

from nextcord.ext import commands
from nextcord.ext.commands import Cog
import nextcord
from nextcord import SlashOption
from nextcord.ext.commands import Bot
import json


# todo: StatCogs
class __StatAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot



def register_stat_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__StatAdminCog(bot))
