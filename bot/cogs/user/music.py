import datetime

import nextwave
from nextcord.ext import commands
from nextcord.ext.commands import Cog
import nextcord
from nextcord import SlashOption
from nextcord.ext.commands import Bot


# todo: MusicCogs
class __MusicUserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name=f'play', description=f'💙 Послухати музло 💛')
    async def play_music(self, interaction: nextcord.Interaction, search: str = SlashOption(
        name="трек",
        description="назва треку, посилання youtube або spotify",
    )):
        search = await nextwave.YouTubeTrack.search(query=search, return_first=True)
        if interaction.user.voice:
            if not interaction.guild.voice_client:
                vc: nextwave.Player = await interaction.user.voice.channel.connect(cls=nextwave.Player)
            elif not getattr(interaction.user.voice, "channel", None):
                embed = nextcord.Embed(
                    title='❌ Спочатку приєднайтеся до голосового каналу:',
                    description='',
                    color=nextcord.Color.dark_purple())
                embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
                embed.set_thumbnail(
                    url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
                embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
                return await interaction.send(embed=embed, ephemeral=True)
            else:
                vc: nextwave.Player = interaction.guild.voice_client

            embed = nextcord.Embed(
                title='🎵 Зараз грає:',
                description='',
                color=nextcord.Color.dark_purple())
            embed.add_field(name=f'Трек: {search.title}', value=f'Автор: **{search.author}**>'[:-1], inline=False)
            embed.add_field(name=f'Link: {search.uri}', value='', inline=False)
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1695657740/music_ydlqjo.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)
            await vc.play(search)
        else:
            embed = nextcord.Embed(
                title='❌ Спочатку приєднайтеся до голосового каналу:',
                description='',
                color=nextcord.Color.dark_purple())
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(name=f'pause', description=f'💙 Поставити музло на паузу 💛')
    async def pause_music(self, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title='❌ Я зараз нічого не співаю.',
                description='Скористайтеся командою: `/play`',
                color=nextcord.Color.dark_purple())
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            return await interaction.send(embed=embed, ephemeral=True)
        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title='❌ Спочатку приєднайтеся до голосового каналу:',
                description='',
                color=nextcord.Color.dark_purple())
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            return await interaction.send(embed=embed, ephemeral=True)
        else:
            vc: nextwave.Player = interaction.guild.voice_client

        await vc.pause()
        embed = nextcord.Embed(
            title='🎵 Музло на паузі:',
            description='Скористайтеся командою: `/resume`',
            color=nextcord.Color.dark_purple())
        embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1695657740/music_ydlqjo.png')
        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(name=f'resume', description=f'💙 Продовжити слухати музло 💛')
    async def resume_music(self, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title='❌ Я зараз нічого не співаю.',
                description='Скористайтеся командою: `/play`',
                color=nextcord.Color.dark_purple())
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            return await interaction.send(embed=embed, ephemeral=True)
        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title='❌ Спочатку приєднайтеся до голосового каналу:',
                description='',
                color=nextcord.Color.dark_purple())
            embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694437277/error_pcueb3.png')
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            return await interaction.send(embed=embed, ephemeral=True)
        else:
            vc: nextwave.Player = interaction.guild.voice_client

        await vc.resume()
        embed = nextcord.Embed(
            title='🎵 Зараз грає:',
            description=f'**{vc.track}**',
            color=nextcord.Color.dark_purple())
        embed.set_image(url='https://res.cloudinary.com/dndstfjbu/image/upload/v1695657740/music_ydlqjo.png')
        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed, ephemeral=True)


def register_music_user_cogs(bot: Bot) -> None:
    bot.add_cog(__MusicUserCog(bot))
