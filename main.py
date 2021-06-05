import discord
from discord.activity import Game
from discord.message import Message

import board_checks
import commands
import database
import embeds

import sqlite3
import random

from discord.utils import get

TOKEN = 'NzgwMzEyNTk5NjA2MzI5MzU0.X7tQvQ.3iCavWuVrwXi-YNyms0eDl825Qg'
client = discord.Client()

##############################################
#Constants
##############################################

GAMES = {}
UPCOMING_GAME_REQUESTS = {}

#############################################
####################SHOP#####################
#############################################

SHOP = {
    'Colors' : {
        'Black':'0',
        'Green':'250',
        'Yellow':'250',
        'White':'0',
        'Purple':'250'
    }
}


@client.event
async def on_ready():
    print('ready', client.user.name)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == '👍':
        print(reaction)
        messageId = UPCOMING_GAME_REQUESTS.get(user.id)
        if messageId == None: return
        if reaction.message.id != messageId[0]: return
        if user.id != messageId[2]: return

        UPCOMING_GAME_REQUESTS[user.id] = None
        BOARD = []

        for i in range(6):
            a = []
            for j in range(7):
                a.append(['black',0])
                
            BOARD.append(a)

        GAMES[messageId[1]] = [user.id, BOARD, 'red', True]
        GAMES[user.id] = [messageId[1], BOARD, 'blue', False]
        await reaction.message.channel.send("Starting game!")
        plr = await client.fetch_user(messageId[1])
        final = board_checks.getBoard(BOARD, plr)
        await reaction.message.channel.send(embed = discord.Embed(title = f"Board {plr.name}'s turn",color = discord.Color.dark_red(), description = final).set_footer(text = 'type ,help for more info'))

    if reaction.emoji == '👎':
        messageId = UPCOMING_GAME_REQUESTS.get(user.id)
        if messageId == None: return
        if reaction.message.id != messageId[0]: return
        
        a = UPCOMING_GAME_REQUESTS[user.id]
        UPCOMING_GAME_REQUESTS[user.id] = None
        UPCOMING_GAME_REQUESTS[a[2]] = None
        await reaction.message.delete()
        plr = await client.fetch_user(a[1])
        await reaction.message.channel.send(f"{plr.mention}, your game request was declined.")

@client.event
async def on_message(message):
    content = message.content
    
    if len(content) > 0 and content[0]==',':
        
        current_word = ''
        for i in content:
            if i==',': continue
            current_word += i
            
            if current_word == 'start': await commands.start(GAMES, UPCOMING_GAME_REQUESTS, message)

            if current_word == 'stop': await commands.stop(GAMES, message)
                
            if current_word == 'help': await message.channel.send(embed=embeds.HELP_EMBED)

            if current_word == 'count': await message.channel.send(f"There is/are {len(GAMES)/1} game(s) being played right now!!!")
            
            if current_word == 'board': await commands.board(GAMES, message, client)
            
            if current_word == 'info': await commands.info(GAMES, message, client)
            
            if current_word == 'insert':
                
                if await commands.insert(GAMES, message)!=None: return
                
                await commands.board(GAMES, message, client)
                                
                await board_checks.checkWinner(GAMES, message, client)


            if current_word == 'stats':
                db1 = database.database()
                db1.createTable()
                Data = db1.getData(message.author.id)
                if Data!=None:
                    await message.channel.send(f'{Data[1]}')
                else:
                    db1.saveData(message.author.id, '0')
                    await message.channel.send(db1.getData(message.author.id)[1])
            
            if current_word == 'save':
                #if not message.author.name == 'az9': return
                db1 = database.database()
                db1.createTable()
                Data = db1.getData(message.author.id)
                abc = message.content.replace(',save ','')
                abc = abc.replace(' ','')
                db1.saveData(message.author.id, abc)
                await message.channel.send(db1.getData(message.author.id)[1])

            if current_word == 'shop':
                launch = message.content.replace(',shop', '')
                launch = launch.replace(' ', '')

                final = launch
                if final == '': return await message.channel.send('Wrong use of commands, Eg.->,shop Colors')
                if SHOP.get(launch):    
                    for i in SHOP[launch]:
                        final = f"{final}\n{i} :{i.lower()}_circle: -> ${SHOP[launch][i]}"
                print(final)
                await message.channel.send(final)

            if current_word == 'buy':
                launch = message.content.replace(',buy', '').replace(' ','')
                final = ''
                #colors white
                print(final, launch)
                for i in launch:
                    final += i
                    print(final)
                    if SHOP.get(final):
                        a = SHOP[final]
                        item = launch.replace(final,'')
                        print(item)
                        if a[item]:
                            db = database.database()
                            db.createTable('backgroundColor')
                            db.createTable()
                            info = db.getData(str(message.author.id))
                            if info !=None:
                                coins = info[1]
                                if int(coins) < int(a[item]): return await message.channel.send('Not enough points')
                            else: return await message.channel.send('Not enough points')
                                
                            abcd = db.saveData(str(message.author.id), item, 'backgroundColor')
                            print(abcd)
                            abc = db.getData(str(message.author.id), 'backgroundColor')
                            print(abc)
                            await message.channel.send(f'Saved Data: {abc[1]}')
                            xyz = db.saveData(message.author.id, str(int(info[1]) - int(a[item])))
                            await message.channel.send(f'{xyz} data for {message.author.name}: ${db.getData(message.author.id)[1]}')
                            break
                        


                    

client.run(TOKEN) 
