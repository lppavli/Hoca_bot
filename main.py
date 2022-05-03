import asyncio
import random
import logging
from requests import get

import discord
from discord.ext import commands

from geo import TOKEN_BOTTES, START_BALANCE
from games.RockScissorsPaper import RockPaperScissorsGame
from games.Coin import CoinGame
from Wallet import Wallet
from WalletDatabaseConnecter import WalletDatabaseConnecter

TOKEN = TOKEN_BOTTES

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

WALLET_CONNECTOR = WalletDatabaseConnecter()

bot = commands.Bot(command_prefix="!!", intents=intents)

wallets = []


@bot.event
async def on_ready():
    global wallets
    wallets = []
    players_without_wallet = find_players_without_wallet(bot, wallets)

    for player_name in players_without_wallet:
        player_balance = WALLET_CONNECTOR.execute_player_balance(player_name)
        print(player_balance)
        if player_balance <= -1:
            WALLET_CONNECTOR.add_player(player_name, START_BALANCE)
            player_balance = WALLET_CONNECTOR.execute_player_balance(player_name)
        wallets.append(Wallet(player=player_name, start_balance=player_balance))
    print(wallets)


@bot.event
async def on_member_join(member):
    if str(member) in find_players_without_wallet(bot, wallets):
        wallets.append(Wallet(player=str(member), start_balance=START_BALANCE))
        if WALLET_CONNECTOR.execute_player_balance(str(member)) <= -1:
            WALLET_CONNECTOR.add_player(member, START_BALANCE)


async def ban_random_member(banned, ctx):
    await banned.kick()

    await ctx.send(banned)

    await asyncio.sleep(5)


async def kick_player(bot, player_name, guild_name):
    player_to_ban = find_player_in_guild(bot, player_name, guild_name)
    try:
        await player_to_ban.kick()
    except AttributeError:
        pass


async def countdown(ctx):
    for i in range(3, 0, -1):

        await ctx.send(str(i))

        await asyncio.sleep(1)


def random_choice_if_not_empty(list):
    if list:
        return random.choice(list)
    return 0


def find_guild(bot, guild_name):
    for guild in bot.guilds:
        if guild == guild_name:
            return guild
    raise AttributeError('Нет такого канала')


def find_player_in_guild(bot, player_name, guild_name):
    guild = find_guild(bot, guild_name)
    for member in guild.members:
        if str(member) == player_name:
            return member
    return False


def find_players_without_wallet(bot, wallets):
    res = []
    for guild in bot.guilds:
        for member in guild.members:
            if member not in wallets:
                res.append(str(member))
    return res


def rps_exchange(game, wallets):
    for i in wallets:
        print(i == game.execute_winner(), 'winner')
        print(i == game.execute_not_winner(), 'not winner')
        print(game.execute_bet())
        if i == game.execute_winner():
            i.add_money(game.execute_bet())
            print(i.execute_balance())
            WALLET_CONNECTOR.save_to_player_balance(game.execute_winner(), i.execute_balance())
        elif i == game.execute_not_winner():
            print(game.execute_bet(), 'bet')
            print(i, 'i')
            i.take_money(game.execute_bet())
            print(i.execute_balance(), 'balance')
            WALLET_CONNECTOR.save_to_player_balance(game.execute_not_winner(), i.execute_balance())


async def show_result_rps(game, wallets):
    if game.can_show_result():
        result, context = game.show_result()
        await context.send(result)
        rps_exchange(game, wallets)


class RandomThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roulette_members = []
        self.rock_paper_scissors_games = []
        wallets = []

    @commands.command(name="help")
    async def help(self, ctx):
        helper_text = """Hola! Это бот, командующий различными мини - играми.
Вот список команд: !!enter - присоедениться к ожиданющим начала русской рулетки,
!!roulette - запустить русскую рулетку
!!start_rps (Ник#Дискриминатор) - бросить вызов игроку в игре камень-ножницы-бумага
!!choose_rps (камень/ножницы/бумага) - выбрать тип атаки в игре камень-ножницы-бумага
        """

        await ctx.send(helper_text)

    @commands.command(name="enter")
    async def add_member(self, ctx):
        self.roulette_members.append(str(ctx.author))

    @commands.command(name="roulette")
    async def roulette(self, ctx):
        if not ctx.author.guild_permissions.kick_members:
            return

        await ctx.send("Играем в рулетку через")

        members_to_ban = self.roulette_members

        await countdown(ctx)

        random_member_to_ban = random_choice_if_not_empty(members_to_ban)

        for _i in range(len(members_to_ban)):
            try:
                if random_member_to_ban:
                    await ban_random_member(random_member_to_ban, ctx)
                    self.roulette_members.remove(random_member_to_ban)
                break
            except AttributeError:
                members_to_ban.remove(random_member_to_ban)
                random_member_to_ban = random_choice_if_not_empty(members_to_ban)

    @commands.command(name="start_rps")
    async def rock_paper_scissors_start(self, ctx, second, bet):
        first_player = str(ctx.author)
        second_player = find_player_in_guild(self.bot, second, ctx.guild)

        if second_player:
            second_player = str(second_player)
            if second_player == first_player:

                await ctx.send("Нельзя играть с самим собой")

            elif first_player not in self.rock_paper_scissors_games and\
                    second_player not in self.rock_paper_scissors_games:
                self.rock_paper_scissors_games.append(RockPaperScissorsGame(first_player, second_player, ctx, bet))

                await ctx.send("Играем в камень-ножницы-бумага")

        else:

            await ctx.send(f"Не могу найти игрока {second}")

    @commands.command(name="choose_rps")
    async def rock_paper_scissors_choose(self, ctx, choice):
        if str(ctx.author) not in self.rock_paper_scissors_games:

            await ctx.send("Вы не учавствуете ни в одной игре в 'камень-ножницы-бумага'")

        else:
            for i in self.rock_paper_scissors_games:
                if i == str(ctx.author):
                    if choice == 'cancel':
                        players = i.execute_players_names()

                        await i.ctx.send(f'Игра {players[0]} против {players[1]} была отменена по решению {ctx.author}')

                        self.rock_paper_scissors_games.remove(i)
                        return
                    i.choose(choice, str(ctx.author))
                    if i.can_show_result():

                        await show_result_rps(i, wallets)

                        self.rock_paper_scissors_games.remove(i)

    @commands.command(name="coin")
    async def coin_game(self, ctx):
        player = str(ctx.author)
        bet = 0
        wallet = Wallet('', 0)
        for i in wallets:

            if i == player:
                bet = i.execute_balance()
                wallet = i

        coin = CoinGame(bet)
        formatted_balacne_after_flip = '{0:,}'.format(coin.determine_balance_after_flip()).replace(',', ' ')

        if coin.get_result():

            await ctx.send(f'{ctx.author}. Вы выйграли. Ваш выйгрыш: {formatted_balacne_after_flip} монеты')

            wallet.add_money(coin.determine_balance_after_flip())
        else:

            await ctx.send(f'{ctx.author}. Вы проиграли. Сумма вашего проигрыша составит'
                           f' {formatted_balacne_after_flip} монеты')

            wallet.take_money(coin.determine_balance_after_flip())
        WALLET_CONNECTOR.save_to_player_balance(player, wallet.execute_balance())

    @commands.command(name="balance")
    async def execute_balance(self, ctx):
        player = str(ctx.author)
        print(wallets)
        for i in wallets:

            if i == player:

                await ctx.send(f'{ctx.author}, ваш баланс: {i.execute_balance()}')

    @commands.command(name='rand_cat')
    async def random_picture(self, ctx):
        is_paid = False
        for i in wallets:
            if i == str(ctx.author):
                print(i.execute_balance())
                if i.execute_balance() < 1000:
                    await ctx.send('У вас недостаточно средств.')
                    return
                else:
                    i.take_money(1000)
                    WALLET_CONNECTOR.save_to_player_balance(str(ctx.author), i.execute_balance())
                    is_paid = True
                print(i.execute_balance())
        if is_paid:
            try:
                source = get(f"https://aws.random.cat/meow").json()
                print(source)
                if source:
                    await ctx.send(source['file'])
                    print(source)
            except Exception:
                await ctx.send("С сервером что-то не то")
        else:
            await ctx.send('Извините, возникли проблемы с оплатой')


bot.remove_command("help")
bot_commands = RandomThings(bot)
bot.add_cog(bot_commands)
bot.run(TOKEN)

