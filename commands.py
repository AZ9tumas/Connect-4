import discord
import ast
import math

import embeds
import board_checks
import database

ERROR_EMBED = embeds.ERROR_EMBED
JOIN_REQUEST_EMBED = embeds.JOIN_REQUEST_EMBED


async def start(GAMES, UPCOMING_GAME_REQUESTS, message):
    if GAMES.get(message.author.id) != None: return await message.channel.send("You're already playing. Type ,stop to stop playing.")
    player = message.mentions[0] if len(message.mentions) > 0 else None
    if player == None: return await message.channel.send(embed=ERROR_EMBED)
    if player == message.author: return await message.channel.send("You can't play with yourself...")
    if GAMES.get(player.id)!=None: return await message.channel.send('That user is already playing with someone else...')
    a = JOIN_REQUEST_EMBED
    a.description = f'{message.author.name} is requesting you, {player.name},  to join them for a game of Connect 4!!!'
    Join_request_message = await message.channel.send(embed = a)
    await message.channel.send(f'{player.name} React to the above message with 👍 to accept or with 👎 to decline.')
    UPCOMING_GAME_REQUESTS[player.id] = [Join_request_message.id, message.author.id, player.id]
    UPCOMING_GAME_REQUESTS[message.author.id] = [Join_request_message.id, message.author.id, player.id]
    await Join_request_message.add_reaction('👍')
    await Join_request_message.add_reaction('👎')

async def stop(GAMES, message, send=True):
    OngoingGame = GAMES.get(message.author.id)
    if OngoingGame==None: return None
    a = GAMES[message.author.id][0]
    GAMES.pop(message.author.id)
    GAMES.pop(a)
    if send==True: await message.channel.send('Stopped :white_check_mark:')

    

async def board(GAMES, message, client):
    OngoingGame = GAMES.get(message.author.id)
    if OngoingGame==None: return
    Board = OngoingGame[1]
    
    #[user.id, BOARD, 'red', True]
    
    idqec = GAMES[OngoingGame[0]][0]
    if OngoingGame[3]==False:
        idqec = OngoingGame[0]

    turn = await client.fetch_user(idqec)
    final = board_checks.getBoard(Board, turn)
    await message.channel.send(embed = discord.Embed(title = f"Board {turn.name}'s turn",color = (OngoingGame[2]=='red' and discord.Color.dark_red() or discord.Color.dark_blue()), description = final).set_footer(text = 'type ,help for more info'))

async def info(GAMES, message, client):
    OngoingGame = GAMES.get(message.author.id)
    if OngoingGame==None: return
    
    plr = await client.fetch_user(OngoingGame[0])
    await message.channel.send(f'You are playing with {plr.name} as {OngoingGame[2].upper()} :{OngoingGame[2]}_circle:')

async def insert(GAMES, message):
    OngoingGame = GAMES.get(message.author.id)
    if OngoingGame==None: return
    Turn = OngoingGame[3]
    if Turn == False: return await message.channel.send('Not your turn.')
    Board = OngoingGame[1]
    Numbers = [int(s) for s in message.content.split() if s.isdigit()]
    RowToInsertCoin = Numbers[0] if len(Numbers)>0 else None
    if RowToInsertCoin==None: return
    RowToInsertCoin -= 1
    if RowToInsertCoin<0: return
    if Board[0][RowToInsertCoin][0] == GAMES[message.author.id][2] or Board[0][RowToInsertCoin][0] == GAMES[GAMES[message.author.id][0]][2]: return
    
    for i in range(len(Board)-1, -1, -1):
        if Board[i][RowToInsertCoin][0] != GAMES[message.author.id][2] and Board[i][RowToInsertCoin][0] != GAMES[GAMES[message.author.id][0]][2]:
            Board[i][RowToInsertCoin][0] = OngoingGame[2]
            Board[i][RowToInsertCoin][1] = message.author.id
            break
        
    
    GAMES[message.author.id][3] = False
    GAMES[GAMES[message.author.id][0]][3] = True
    GAMES[message.author.id][1] = Board
    GAMES[GAMES[message.author.id][0]][1] = Board
    OngoingGame = GAMES.get(message.author.id)
    if OngoingGame==None: return

async def matches(message, page=1, view=0, player=None):
    player = player != None and player or message.author
    db = database.database()
    db.createTable('matches', ['user','points'])
    Data = db.getData(player.id, 'matches')
    Data = Data != None and Data[1] or {}
    Data = ast.literal_eval(str(Data))

    counter = 0

    print(page, view)

    if view <= len(Data) and view>0:
        for i in Data:
            counter += 1
            if counter == view:
                info = Data.get(i)
                EMBED = discord.Embed(
                    title = i,
                    color = discord.Color.dark_gold(),
                    description = board_checks.getBoard(info.get('Board'))
                )
                EMBED.set_footer(text = f"{info.get('Winner')} won the match")
                await message.channel.send(embed = EMBED)
                return
        await message.channel.send(f"{player.name} hasn't played that many matches...")

    elif view > 0:
        return await message.channel.send(f"Match {view} doesn't exist")

    #Data[title] = {['Winner'] : message.author.name, ['Board'] : Board}
    print('EeeeeEeeEeEeEEeeEeeeeEe')

    start = (page * 10) - 9
    MAX = 9 + start

    final = ''
    
    if len(Data) < start: print('eeeeNONONO');return await message.channel.send(f"{player.name} hasn't played that many matches...")

    for i in Data:
        counter +=1

        if counter < start: continue
        

        text = f'{counter}. {i}\n'
        final += text

        if counter >= MAX: break
    EMBED = discord.Embed(title = 'Matches', description = final, color = discord.Color.dark_orange())
    EMBED.set_footer(text=f'Page {page} of {math.ceil(len(Data)/10)}')
    await message.channel.send(embed = EMBED)

async def stats(message):
    db1 = database.database()
    db1.createTable()
    Data = db1.getData(message.author.id)
    if Data!=None:
        await message.channel.send(f'{Data[1]}')
    else:
        db1.saveData(message.author.id, '0')
        await message.channel.send(db1.getData(message.author.id)[1])

async def saveboard(player2, Board, player1):

    db1 = database.database()

    db1.createTable('matches', ['user','points'])
    Data = db1.getData(str(player1['Id']), 'matches')
    
    Data = Data != None and Data[1] or {}

    if isinstance(ast.literal_eval(str(Data)), list): Data = {}

    Data = ast.literal_eval(str(Data))

    title = f"{player1['Name']} vs {player2['Name']}"
    temp = title
    counter = 1
    
    while Data.get(title) != None:
        counter += 1
        title = f'{temp} {counter}'

    Data[title] = {'Winner' : player1['Name'], 'Board' : Board}
    
    db1.saveData(player1['Id'], str(Data), 'matches')
    print("SAVED BOARD SUCCESSFULLY")
