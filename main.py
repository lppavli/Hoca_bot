import discord
from discord.ext import commands

import asyncio
import random
import logging

from geo import TOKEN_BOTTES, START_BALANCE
from rps import RockPaperScissorsGame
from coin import CoinGame
from wallet import Wallet
from WalletDatabaseConnector import WalletDatabaseConnector

TOKEN = TOKEN_BOTTES

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

WALLET_CONNECTOR = WalletDatabaseConnector()


async def ban_random_member(banned, ctx):
    await banned.kick()
    await ctx.send(banned)
    await asyncio.sleep(5)


async def kick_player(bot, player_name, guild_name):
    player_to_ban = find_player(bot, player_name, guild_name)
    try:
        await player_to_ban.kick()
    except Exception:
        print(player_to_ban)


async def countdown(ctx):
    for i in range(3, 0, -1):
        await ctx.send(str(i))
        await asyncio.sleep(1)


def random_choice_if_not_empty(list):
    if list:
        return random.choice(list)


def find_player(bot, player_name, guild_name):
    try:
        for guild in bot.guilds:
            if guild == guild_name:
                for member in guild.members:
                    if str(member) == player_name:
                        return member
        raise Exception('В данном чате нет этого игрока')
    except Exception:
        return ''


async def show_result_rps(games, ctx):
    for i in games:
        if i == str(ctx.author):
            await ctx.send(i.show_result())

            if i.not_winner:
                await kick_player(bot, i.not_winner, ctx.guild)
            else:
                for j in i.get_players():
                    await kick_player(bot, j, ctx.guild)

                await ctx.send('Слабакам тут не место.')


class RandomThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_members = []
        self.rock_paper_scissors_games = []
        self.wallets = []

    @commands.command(name="help")
    async def help(self, ctx):
        helper_text = """Hola! Это бот, командующий различными мини - играми.
Вот список команд: !!enter - присоедениться к ожиданющим начала русской рулетки,
!!roulette - запустить русскую рулетку
!!start_rps (Ник#Дискриминатор) - бросить вызов игроку в игре камень-ножницы-бумага
!!choose_rps (камень/ножницы/бумага) - выбрать тип атаки в игре камень-ножницы-бумага
        """
        await ctx.send(helper_text)

    @commands.command(name="get_balances")
    async def set_players_wallets(self, ctx):
        for guild in self.bot.guilds:
            for member in guild.members:
                if member not in self.wallets:
                    player_name = str(member)

                    player_balance = WALLET_CONNECTOR.execute_player_balance(player_name)

                    if player_balance > -1:
                        self.wallets.append(Wallet(player=str(member), start_balance=player_balance))
                    else:
                        self.wallets.append(Wallet(player=str(member), start_balance=START_BALANCE))
                        WALLET_CONNECTOR.add_player(str(member))

        print(self.wallets)

    @commands.command(name="enter")
    async def add_member(self, ctx):
        self.game_members.append(str(ctx.author))

    @commands.command(name="roulette")
    async def roulette(self, ctx):
        await ctx.send(f"Играем в рулетку через")
        members_to_ban = self.game_members
        await countdown(ctx)
        random_member_to_ban = random_choice_if_not_empty(members_to_ban)

        for i in range(len(members_to_ban)):
            try:
                if random_member_to_ban:
                    await ban_random_member(random_member_to_ban, ctx)
                    self.game_members.remove(random_member_to_ban)
                break
            except Exception:
                members_to_ban.remove(random_member_to_ban)
                random_member_to_ban = random_choice_if_not_empty(members_to_ban)
        print(self.game_members)

    @commands.command(name="start_rps")
    async def rock_paper_scissors(self, ctx, second):
        first_player = str(ctx.author)
        second_player = str(find_player(bot, second, ctx.guild))

        if second_player:
            if second_player == first_player:
                await ctx.send("Нельзя играть с самим собой")
                return
            elif first_player not in self.rock_paper_scissors_games and\
                    second_player not in self.rock_paper_scissors_games:

                self.rock_paper_scissors_games.append(RockPaperScissorsGame(first_player, second_player, ctx.guild))
                await ctx.send(f"Играем в камень-ножницы-бумага")

        else:
            await ctx.send(f"Не могу найти игрока {second}")

        print(self.rock_paper_scissors_games)

    @commands.command(name="choose_rps")
    async def choose_rps(self, ctx, choice):
        if str(ctx.author) not in self.rock_paper_scissors_games:
            await ctx.send("Вы не учавствуете ни в одной игре в 'камень-ножницы-бумага'")
        else:
            for i in self.rock_paper_scissors_games:
                if i == str(ctx.author):
                    i.choose(choice, str(ctx.author))
                    if i.can_show_result(ctx.guild):
                        await show_result_rps(self.rock_paper_scissors_games, ctx)
                        self.rock_paper_scissors_games.remove(i)

        print(self.rock_paper_scissors_games)

    @commands.command(name="coin")
    async def coin_game(self, ctx):
        player = str(ctx.author)
        bet = 0
        wallet = 0
        for i in self.wallets:
            print(i)
            if i == player:
                bet = i.get_balance()
                print(i)
                wallet = i

        coin = CoinGame(bet)
        print(bet)
        print(coin.get_result())
        if coin.get_result():
            await ctx.send(f'Вы выйграли. Ваш выйгрыш: {coin.determine_balance_after_flip()} монеты')
            wallet.add_money(coin.determine_balance_after_flip())
        else:
            await ctx.send(f'Вы проиграли. Сумма вашего проигрыша составит'
                           f' {coin.determine_balance_after_flip()} монеты')
            wallet.take_money(coin.determine_balance_after_flip())
        print(self.wallets)
        for i in self.wallets:
            print(i.get_balance())


bot = commands.Bot(command_prefix="!!", intents=intents)
bot.remove_command("help")
bot.add_cog(RandomThings(bot))
bot.run(TOKEN)
