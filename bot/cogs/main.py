from nextcord.ext.commands import Bot
from bot.cogs.admin import register_admin_cogs
from bot.cogs.other import register_other_cogs
from bot.cogs.user import register_user_cogs
from bot.cogs.admin.team import register_team_admin_cogs
from bot.cogs.user.github import register_github_cogs


def register_all_cogs(bot: Bot) -> None:
    cogs = (
        register_user_cogs,
        register_admin_cogs,
        register_other_cogs,
        register_team_admin_cogs,
        register_github_cogs,
    )
    for cog in cogs:
        cog(bot)
