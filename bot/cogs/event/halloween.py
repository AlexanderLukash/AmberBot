import asyncio
from PIL import Image
from easy_pil import load_image_async, Editor
from nextcord.ext.commands import Cog
import nextcord
from nextcord.ext.commands import Bot
import json
import cloudinary
import random
from cloudinary import uploader

cloudinary.config(
    cloud_name="dndstfjbu",
    api_key="399658246291491",
    api_secret="lSMOzkIj3JUOnNpZ0rvHz9pIDC4"
)

halloween_emoji = ["👻", "🎃", "🦇", "🕷️", "🪦", "💀", "🌙", "🕸️"]

halloween_quotes = [
    "Зачини двері, запали свічку, і через вікно ведмедицю не впускай.",
    "У цю ніч навіть гарбузи можуть стати чарівними каретами.",
    "Як і будь-яке закляття, Хеллоуїн починається з 'Вау!'",
    "Забудьте про калорії та подарунки - Хеллоуїн - це час жахливо смачних ласощів.",
    "Навіть привидам потрібно відпочити і погуляти. Особливо на Хеллоуїн.",
    "У цю ніч навіть місяць посміхається зловісно.",
    "Не бійтеся темряви - це просто відсутність світла, але іноді там можуть ховатися смішні жахи",
    "Хеллоуїн - це єдиний час у році, коли ви можете носити свої страхи як костюми.",
    "На Хеллоуїн ніч земля стає живою, а мертві речі оживають.",
    "Нехай кожен уловить свою зірку з неба, а Хеллоуїн нехай принесе свої мрії.",
    "Знайдіть своїм душам світло серед цієї ночі.",
    "Ніч Хеллоуїну - це ніч, коли мрії стають кошмарами і кошмари стають справжністю.",
    "У цю ніч вітер шепоче секрети, а тьма приховує найбільші чари.",
    "Ніч Хеллоуїну - це час, коли ми всі стаємо трохи чарівними.",
    "Смерть не кінець історії, а лише початок нового розділу.",
    "Відьми мають свої секрети, але Хеллоуїн - це час поділитися ними.",
    "На Хеллоуїн ніч небо більш ясне, а зірки ближче.",
    "Таємниця Хеллоуїну полягає в тому, що все можливо.",
    "На Хеллоуїн ніч стає днем для всіх тих, хто вірить у дива.",
    "Хеллоуїн - це час, коли душі мертвих повертаються, щоб зустрітися з живими."
]

candy_count_list = [3, 1, 5, 7, 2, 1, 4, 6, 2, 8, 1, 1, 2, 3]

class AnswerButtons(nextcord.ui.View):


    def __init__(self, correct_answer):
        super().__init__(timeout=7200)
        self.value = None
        self.correct_answer = correct_answer

    @nextcord.ui.button(label="1", style=nextcord.ButtonStyle.gray)
    async def first_ansver(self, buttun: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.correct_answer == 0:
            self.value = True

            file_name = "halloween_users.json"

            try:
                # Load current data from the file (if available)
                with open(file_name, 'r') as file:
                    data = json.load(file)

            except FileNotFoundError:
                # If no file is found, create an empty dictionary
                data = {}
            if str(interaction.user.id) in data:
                candy = data[str(interaction.user.id)][1]['candy']
                candy_added = random.choice(candy_count_list)
                new_candy = candy + candy_added
                data[str(interaction.user.id)][1]['candy'] = new_candy

                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)

            await interaction.send(f"True; You give: {candy_added} Candy: {data[str(interaction.user.id)][1]['candy']}", ephemeral=True)
        else:
            self.value = False
            await interaction.send('False', ephemeral=True)

    @nextcord.ui.button(label="2", style=nextcord.ButtonStyle.gray)
    async def second_ansver(self, buttun: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.correct_answer == 1:
            self.value = True

            file_name = "halloween_users.json"

            try:
                # Load current data from the file (if available)
                with open(file_name, 'r') as file:
                    data = json.load(file)

            except FileNotFoundError:
                # If no file is found, create an empty dictionary
                data = {}
            if str(interaction.user.id) in data:
                candy = data[str(interaction.user.id)][1]['candy']
                candy_added = random.choice(candy_count_list)
                new_candy = candy + candy_added
                data[str(interaction.user.id)][1]['candy'] = new_candy

                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)

            await interaction.send(f"True; Candy: {data[str(interaction.user.id)][1]['candy']}", ephemeral=True)
        else:
            self.value = False
            await interaction.send('False', ephemeral=True)

    @nextcord.ui.button(label="3", style=nextcord.ButtonStyle.gray)
    async def third_ansver(self, buttun: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.correct_answer == 2:
            self.value = True

            file_name = "halloween_users.json"

            try:
                # Load current data from the file (if available)
                with open(file_name, 'r') as file:
                    data = json.load(file)

            except FileNotFoundError:
                # If no file is found, create an empty dictionary
                data = {}
            if str(interaction.user.id) in data:
                candy = data[str(interaction.user.id)][1]['candy']
                candy_added = random.choice(candy_count_list)
                new_candy = candy + candy_added
                data[str(interaction.user.id)][1]['candy'] = new_candy

                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)

            await interaction.send(f"True; Candy: {data[str(interaction.user.id)][1]['candy']}", ephemeral=True)
        else:
            self.value = False
            await interaction.send('False', ephemeral=True)

    @nextcord.ui.button(label="4", style=nextcord.ButtonStyle.gray)
    async def fourth_ansver(self, buttun: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.correct_answer == 3:
            self.value = True

            file_name = "halloween_users.json"

            try:
                # Load current data from the file (if available)
                with open(file_name, 'r') as file:
                    data = json.load(file)

            except FileNotFoundError:
                # If no file is found, create an empty dictionary
                data = {}
            if str(interaction.user.id) in data:
                candy = data[str(interaction.user.id)][1]['candy']
                candy_added = random.choice(candy_count_list)
                new_candy = candy + candy_added
                data[str(interaction.user.id)][1]['candy'] = new_candy

                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=4)

            await interaction.send(f"True; Candy: {data[str(interaction.user.id)][1]['candy']}", ephemeral=True)

        else:
            self.value = False
            await interaction.send('False', ephemeral=True)

class __HalloWeenCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name=f'halloween', description=f'🎃 Цукерки або смерть! 👻')
    async def halloween(self, interaction: nextcord.Interaction):
        file_name = "halloween_users.json"

        try:
            # Load current data from the file (if available)
            with open(file_name, 'r') as file:
                data = json.load(file)

        except FileNotFoundError:
            # If no file is found, create an empty dictionary
            data = {}

        back = Image.new('RGBA', ((512, 472)))
        back = Editor(back)
        background = Editor(f"Group 651.png").resize((512, 281))
        profile = await load_image_async(str(interaction.user.avatar.url))
        profile = Editor(profile).resize((343, 343)).rounded_corners(radius=25)
        background_1 = Editor(f"Group 652.png").resize((512, 147))
        back.paste(background.image, (0, 0))
        back.paste(profile.image, (70, 50))
        back.paste(background_1.image, (-10, 310))
        back.save("halloween_avatar.png")
        result = cloudinary.uploader.upload("halloween_avatar.png",
                                            public_id="halloween_avatar")

        if str(interaction.user.id) in data:
            embed = nextcord.Embed(
                title='🎃 Цукерки або смерть! 🎃',
                description=f'**{random.choice(halloween_quotes)}**',
                color=nextcord.Color.dark_purple())
            embed.set_thumbnail(
                url=f'https://res.cloudinary.com/dndstfjbu/image/upload/v1696921147/Group_135_qdrmsc.png')
            embed.add_field(name=f"🍬 Цукерок: **{data[str(interaction.user.id)][1]['candy']}**", value=f"",
                            inline=False)
            embed.set_image(url=f"{result['url']}")
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)

        elif str(1047938410347765911) in data:
            pass

        else:
            data[interaction.user.id] = interaction.user.name, {'candy': 0}

            # Записываем обновленные данные в файл
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)

            with open(file_name, 'r') as file:
                data = json.load(file)

            embed = nextcord.Embed(
                title='🎃 Цукерки або смерть! 🎃',
                description=f'**{random.choice(halloween_quotes)}**',
                color=nextcord.Color.dark_purple())
            embed.add_field(name=f"🍬 Цукерок: **{data[str(interaction.user.id)][1]['candy']}**", value=f"",
                            inline=False)
            embed.set_thumbnail(
                url='https://res.cloudinary.com/dndstfjbu/image/upload/v1696921147/Group_135_qdrmsc.png')
            embed.set_image(url=f"{result['url']}")
            embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.send(embed=embed, ephemeral=True)

    @nextcord.slash_command(name=f'halloween_top', description=f'🎃 Хто зібрав найбільше солодощів? 👻')
    async def halloween_top(self, interaction: nextcord.Interaction):
        file_name = "halloween_users.json"

        try:
            # Load current data from the file (if available)
            with open(file_name, 'r') as file:
                data = json.load(file)

        except FileNotFoundError:
            # If no file is found, create an empty dictionary
            data = {}

        top_user = sorted(data.items(), key=lambda x: x[1][1]['candy'], reverse=True)
        top_ten = top_user[:10]
        embed = nextcord.Embed(
            title='🎃 Топ збирачів! 🎃',
            description=f'**Наздоганяй їх скоріше!**',
            color=nextcord.Color.dark_purple())

        for i, (user_id) in enumerate(top_ten, start=1):
            name = user_id[1][0]
            candy = user_id[1][1]["candy"]
            embed.add_field(name=f"{random.choice(halloween_emoji)} **{name}**", value=f"🍬 Цукерок: **{candy}**",
                            inline=False)
            embed.add_field(name='', value='')

        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1696921147/Group_135_qdrmsc.png')
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed, ephemeral=True)

    # @nextcord.slash_command(name=f'halloween_quiz', description=f'🎃 Хто зібрав найбільше солодощів? 👻')
    async def halloween_quiz(self):
        interaction = nextcord.Interaction
        file_name = "halloween_quiz.json"

        try:
            # Load current data from the file (if available)
            with open(file_name, 'r') as file:
                data = json.load(file)

        except FileNotFoundError:
            # If no file is found, create an empty dictionary
            data = {}

        quiz = random.choice(data['quizs'])
        channel = self.bot.get_channel(1161175049798160455)
        embed = nextcord.Embed(
            title=f'🎃 {quiz["quiz"]} 🎃',
            description=f'Обери 1 правильну відповідь!',
            color=nextcord.Color.dark_purple())
        for choice, answer in enumerate(quiz["answers"]):
            embed.add_field(name=f'**{choice + 1}. {answer["answer"]}**', value='', inline=False)
        correct_answer = next((i for i, answer in enumerate(quiz["answers"]) if answer["correct"]), None)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(
            url='https://res.cloudinary.com/dndstfjbu/image/upload/v1696921147/Group_135_qdrmsc.png')
        view = AnswerButtons(correct_answer)
        await channel.send(embed=embed, view=view)

    @Cog.listener()
    async def on_ready(self):
        while True:
            await self.halloween_quiz()
            await asyncio.sleep(7200)


def register_halloween_event_cogs(bot: Bot) -> None:
    bot.add_cog(__HalloWeenCog(bot))
