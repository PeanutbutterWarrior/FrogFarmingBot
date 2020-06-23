from discord.ext import commands
import random

with open('token', 'r') as file:
    TOKEN = file.read()

GUILD = 'Bot Testing'

FROGCOST = 2
FROGVALUE = 1
PONDCOST = 10
PONDSIZE = 10

bot = commands.Bot(command_prefix='!', case_insensitive=True)

users = {}

# £


def userInDictCheck(ctx):
    if ctx.author not in users:
        users[ctx.author] = {'money': 100, 'frogs': 0, 'ponds': 0}

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f'I\'m in {guild.name}')
    print(f'{bot.user} has connected to Discord')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        print(f'{ctx.author} error, missing arg(s)')
    elif isinstance(error, commands.errors.BadArgument):
        print(f'{ctx.author} error, bad arg(s)')


@bot.command(name='farm')
async def farm(ctx):
    await ctx.send(f'{str(ctx.author)[:-5]} farmed {random.randint(10, 21)} frogs')


@bot.command(name='buy')
async def buy(ctx, item='', *args):
    if item == 'frog':
        await buyFrogs(ctx, int(args[0]))
    elif item == 'pond':
        await buyPonds(ctx, int(args[0]))


@bot.command(name='sell')
async def sell(ctx, item='', *args):
    if item == 'frog':
        await sellFrogs(ctx, int(args[0]))


async def buyFrogs(ctx, amount):
    userInDictCheck(ctx)
    if amount <= 0:
        await ctx.send(f'{str(ctx.author)[:-5]}, no buying antimatter frogs allowed')
    elif users[ctx.author]['money'] < amount * FROGCOST:
        await ctx.send(f'{str(ctx.author)[:-5]}, you do not have enough money to buy {amount} frogs for £{amount * FROGCOST}')
    elif users[ctx.author]['frogs'] + amount > users[ctx.author]['ponds'] * PONDSIZE:
        await ctx.send(f'{str(ctx.author)[:-5]}, you bought {users[ctx.author]["frogs"] + amount - users[ctx.author]["ponds"] * PONDSIZE}'
                       f' too many frogs, you can only store {users[ctx.author]["ponds"] * PONDSIZE}')
    else:
        users[ctx.author]['money'] -= amount * FROGCOST
        users[ctx.author]['frogs'] += amount
        await ctx.send(f'{str(ctx.author)[:-5]}, you bought {amount} frogs for £{amount * FROGCOST}')


async def sellFrogs(ctx, amount):
    userInDictCheck(ctx)
    if amount <= 0:
        await ctx.send(f'{str(ctx.author)[:-5]}, No antimatter frogs allowed')
    elif users[ctx.author]['frogs'] < amount:
        await ctx.send(f'{str(ctx.author)[:-5]}, you do not have enough frogs')
    else:
        users[ctx.author]['money'] += amount * FROGVALUE
        users[ctx.author]['frogs'] -= amount
        await ctx.send(f'{str(ctx.author)[:-5]}, you sold {amount} frogs for £{amount * FROGVALUE}')


async def buyPonds(ctx, amount):
    userInDictCheck(ctx)
    if amount < 0:
        await ctx.send(f'{str(ctx.author)[:-5]}, no buying antimatter ponds')
    elif users[ctx.author]['money'] < amount * PONDCOST:
        await ctx.send(f'{str(ctx.author)[:-5]}, you do not have enough money to buy {amount} ponds for £{amount * PONDCOST}')
    else:
        users[ctx.author]['money'] -= amount * PONDCOST
        users[ctx.author]['ponds'] += amount
        await ctx.send(f'{str(ctx.author)[:-5]}, you bought {amount} ponds for £{amount * PONDCOST}')


@bot.command(name='balance', aliases=['bal'])
async def balance(ctx):
    userInDictCheck(ctx)
    await ctx.send(f'{str(ctx.author)[:-5]}, your balance is £{users[ctx.author]["money"]} and you have {users[ctx.author]["frogs"]} frogs')


bot.run(TOKEN)
