import time
from nextcord.ext import commands
from nextcord.ext.commands import Cog
import nextcord
from nextcord import SlashOption
from nextcord.ext.commands import Bot


# todo: TicketsCogs


class AddUser(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Додати Учасника до Приватного Чату",
            timeout=300,
        )
        self.channel = channel
        self.user = nextcord.ui.TextInput(
            label="Учасник", min_length=2, max_length=30, required=True,
            placeholder="Ідентифікатор користувача(ID) (має бути int)"
        )
        self.add_item(self.user)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return await interaction.send('Недійсний користувач.', ephemeral=True)
        overwrites = nextcord.PermissionOverwrite()
        overwrites.read_messages = True
        await self.channel.set_permissions(user, overwrite=overwrites)
        await interaction.send(f'{user.mention} був доданий до цього приватного чату.')


class RemoveUser(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Видалити Учасника з Приватного Чату",
            timeout=300,
        )
        self.channel = channel
        self.user = nextcord.ui.TextInput(
            label="Учасник", min_length=2, max_length=30, required=True,
            placeholder="Ідентифікатор користувача(ID) (має бути int)"
        )
        self.add_item(self.user)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = interaction.guild.get_member(int(self.user.value))
        if user is None:
            return await interaction.send('Недійсний користувач.', ephemeral=True)
        overwrites = nextcord.PermissionOverwrite()
        overwrites.read_messages = False
        await self.channel.set_permissions(user, overwrite=overwrites)
        await interaction.send(f'{user.mention} був видалений з цього приватного чату.')


class CreateTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Написати Нам", emoji='📩', style=nextcord.ButtonStyle.blurple,
                        custom_id="create_ticket:blurple")
    async def create_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = await interaction.send("Приватний канал скоро буде створений...", ephemeral=True)

        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            interaction.guild.get_role(1003930238599843903): nextcord.PermissionOverwrite(read_messages=True)
        }

        category_channel = nextcord.utils.get(interaction.guild.categories, id=1158784089093062757)
        channel = await interaction.guild.create_text_channel(f'{interaction.user.name} - ticket',
                                                              overwrites=overwrites, category=category_channel)
        await msg.edit(f'Приватний канал створено! Починайте спілкування: {channel.mention}')
        embed = nextcord.Embed(title="Залиш Своє Повідомлення Тут",
                               description=f'{interaction.user.mention} Наша команда відповість вам дуже скоро. Почекайте трошки 📨',
                               colour=nextcord.Color.dark_purple())
        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        embed.set_footer(text="З повагою | AMBER",
                         icon_url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        await channel.send(embed=embed, view=TicketSettings())


class TicketSettings(nextcord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Додати Учасника', style=nextcord.ButtonStyle.green, emoji='🫂',
                        custom_id='ticket_setting:green')
    async def ticket_add_user(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(AddUser(interaction.channel))

    @nextcord.ui.button(label='Вигнати учасника', style=nextcord.ButtonStyle.gray, emoji='🫂',
                        custom_id='ticket_setting:gray')
    async def ticket_remove_user(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(RemoveUser(interaction.channel))

    @nextcord.ui.button(label='Закінчити розмову', style=nextcord.ButtonStyle.red, emoji='🔒',
                        custom_id='ticket_setting:red')
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.send(
            'Дякуємо, що звернулися до нас. Наша команда бажає вам гарного дня ✨\nКанал буде видалений за декілька секунд...',
            ephemeral=True)
        time.sleep(5)
        await interaction.channel.delete()


class __TicketsAdminCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name=f'setup_ticket', description=f'💙 Створити тікет 💛')
    @commands.has_permissions(manage_guild=True)
    async def setup_ticket(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel,
                           title: str = SlashOption(
                               name="заголовок",
                               description="напишіть заголовок",
                           ), description: str = SlashOption(
                name="опис",
                description="опишіть для чого цей тікет",
            )):
        embed = nextcord.Embed(title=title, description=description, colour=nextcord.Color.dark_purple())
        embed.set_footer(text="Написніть на кнопку нижче | AMBER",
                         icon_url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        await channel.send(embed=embed, view=CreateTicket())
        embed = nextcord.Embed(title='Тікет успішно ствонерий 📩',
                               description=f'Ви можете переглянути його в каналі: {channel.mention}',
                               colour=nextcord.Color.dark_purple())
        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1694435809/001_1-3000x3000_1_fzv705.png')
        await interaction.send(embed=embed, ephemeral=True)


def register_tickets_admin_cogs(bot: Bot) -> None:
    bot.add_cog(__TicketsAdminCog(bot))
