import discord

TOKEN = 'NzgwMzEyNTk5NjA2MzI5MzU0.X7tQvQ.3iCavWuVrwXi-YNyms0eDl825Qg'
client = discord.Client()

###########################
#########EMBEDS############
###########################

ERROR_EMBED = discord.Embed(
    title = 'Error',
    color = discord.Color.dark_gold(),
    description = 'No player mentioned. Please mention a player in order to play with them.\nExample: ,start @ThONk'
)

ERROR_EMBED.set_footer(text='Better luck next time...')
ERROR_EMBED.set_image(url = 'https://rockcontent.com/wp-content/uploads/2021/02/stage-en-error-1020.png')

JOIN_REQUEST_EMBED = discord.Embed(
    title = 'Join request - react with 👍 to accept or with 👎 to decline.',
    color = discord.Color.dark_orange(),
    description = 'x is requesting you, y,  to join them for a game of Connect 4!!!'
)

JOIN_REQUEST_EMBED.set_image(url = 'https://media.discordapp.net/attachments/790093082515079169/834014685032349696/unknown.png')
JOIN_REQUEST_EMBED.set_footer(text='Type ,help to know how to play.')

HELP_EMBED = discord.Embed(
    title = 'Help - How to play Connect 4 using ThONk',
    description = 'The two players then alternate turns dropping one of their discs at a time into an unfilled column, until the second player, with red discs, achieves a four in a row, and wins the game.\n If the board fills up before either player achieves four in a row, then the game is a draw. \n\n\nType ,start @mention to start playing Connect 4 with someone. Use commands ,insert 1 to insert the coin into a specific row.\n',
    color = discord.Color.red()
)

HELP_EMBED.set_image(url = 'https://media.discordapp.net/attachments/762774251841257495/834002032561356810/unknown.png')
HELP_EMBED.set_footer(text='Type ,count to know how many players are playing the game right now!')
#############################################
#FUNCTIONS
#############################################

def getBoard(Board):
    final = ''
    #print(Board)
    for i in Board:
        a = i
        for j in a:
            final += f':{j[0]}_circle:'
        final += '\n'
    return final

async def checkHorizontal(Board, message):
    '''
    [
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]]
    ]
    '''

    counter = {
        GAMES[message.author.id][2] : 0,
        GAMES[GAMES[message.author.id][0]][2] : 0
    }
    for row in Board:
        for coin in row:
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]:
                counter = {
                    GAMES[message.author.id][2] : 0,
                    GAMES[GAMES[message.author.id][0]][2] : 0
                }
                continue
            otherColor = coin[0]!=GAMES[GAMES[message.author.id][0]][2] and GAMES[GAMES[message.author.id][0]][2] or GAMES[message.author.id][2]
            
            counter[coin[0]] += 1
            counter[otherColor] = 0

            if counter[coin[0]]>= 4: return True, coin[0],await client.fetch_user(coin[1])
    return False, None, None

async def checkVertical(Board, message):
    '''
    [
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]]
    ]
    '''

    counter = {
        GAMES[message.author.id][2] : 0,
        GAMES[GAMES[message.author.id][0]][2] : 0
    }
    
    for i in range(0,7):
        for j in range(0,6):
            coin = Board[j][i]
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]:
                counter = {
                    GAMES[message.author.id][2] : 0,
                    GAMES[GAMES[message.author.id][0]][2] : 0
                }
                continue
            otherColor = coin[0]!=GAMES[GAMES[message.author.id][0]][2] and GAMES[GAMES[message.author.id][0]][2] or GAMES[message.author.id][2]
            
            counter[coin[0]] += 1
            counter[otherColor] = 0

            if counter[coin[0]]>= 4: return True, coin[0],await client.fetch_user(coin[1])
        
                

    return False, None, None

def getAt(Board, Row, CoinNumber):
    
    if Row < len(Board) and CoinNumber < len(Board[Row]):
        
        return Board[Row][CoinNumber]
    
    return None

def checkDirection(Board, Row, CoinNumber, RowIncr, CoinIncr):
    coin = getAt(Board, Row, CoinNumber)

    counter = 0
    currentCoin, CurrentRow, CurrentCoinNumber = coin,Row,CoinNumber
    
    while counter<4:
        print(currentCoin, CurrentRow, CurrentCoinNumber, counter)
        if currentCoin != None and currentCoin == coin:
            counter += 1
        else:
            return False
        
        CurrentCoinNumber+= CoinIncr
        CurrentRow += RowIncr
        currentCoin = getAt(Board, CurrentRow, CurrentCoinNumber)
    print(counter)
    return True

async def checkDiagonal(Board, message):
    '''
    [
    [['white', 0], ['white', 0], ['white', 0], [' red ', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], [' red ', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], [' red ', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [[' red ', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]], 
    [['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0], ['white', 0]]
    ]
    '''

    
    for i in range(7):
        for j in range(6):
            coin = getAt(Board, j, i)
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]: continue

            UpperCheck = checkDirection(Board, j, i, -1, 1)
            LowerCheck = checkDirection(Board, j, i, 1, 1)

            print(UpperCheck, LowerCheck)
            
            if LowerCheck==True or UpperCheck == True:
                return True, coin[0], await client.fetch_user(coin[1])

    return False, None, None

##############################################
#keep a track of the games and upcoming games#
##############################################

GAMES = {}
UPCOMING_GAME_REQUESTS = {}

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
        final = getBoard(BOARD)
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
            
            if current_word == 'start':
                if GAMES.get(message.author.id)!=None: return await message.channel.send("You're already playing. Type ,stop to stop playing.")
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

            if current_word == 'stop':
                OngoingGame = GAMES.get(message.author.id)
                if OngoingGame==None: return
                a = GAMES[message.author.id][0]
                GAMES.pop(message.author.id)
                GAMES.pop(a)
                await message.channel.send('Stopped :white_check_mark:')
            if current_word == 'help': await message.channel.send(embed=HELP_EMBED)
            if current_word == 'count': await message.channel.send(f"There are {len(GAMES)/1} game(s) being played right now!!!")
            if current_word == 'board':
                OngoingGame = GAMES.get(message.author.id)
                if OngoingGame==None: return
                Board = OngoingGame[1]
                final = getBoard(Board)
                #[user.id, BOARD, 'red', True]
                
                idqec = GAMES[OngoingGame[0]][0]
                if OngoingGame[3]==False:
                    idqec = OngoingGame[0]

                turn = await client.fetch_user(idqec)
                await message.channel.send(embed = discord.Embed(title = f"Board {turn.name}'s turn",color = discord.Color.dark_red(), description = final).set_footer(text = 'type ,help for more info'))
            if current_word == 'insert':
                OngoingGame = GAMES.get(message.author.id)
                if OngoingGame==None: return
                Turn = OngoingGame[3]
                if Turn == False: return await message.channel.send('Not your turn.')
                Board = OngoingGame[1]
                Numbers = [int(s) for s in content.split() if s.isdigit()]
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
                final = getBoard(OngoingGame[1])
                abc = await client.fetch_user(OngoingGame[0])
                
                await message.channel.send(embed = discord.Embed(title = f"Board - {abc.name}'s turn",color = discord.Color.dark_red(), description = final).set_footer(text = 'type ,help for more info'))
                
                h, hwc,pId1 = await checkHorizontal(Board, message)
                v, vwc,pId2 = False, None, None
                d, dwc,pId3 = False, None, None
                if h == False:
                    v, vwc,pId2 = await checkVertical(Board, message)
                if h==False and v==False:
                    d, dwc,pId3 = await checkDiagonal(Board, message)
                
                print(h, v, d)
                finalWinner, fwc, fpId = False, None, None
                Direction = ''
                if h==True:
                    finalWinner, fwc, fpId = h, hwc, pId1
                    Direction = 'Horizontal'
                if v==True:
                    finalWinner, fwc, fpId = v, vwc, pId2
                    Direction = 'Vertical'
                if d==True:
                    finalWinner, fwc, fpId = d, dwc, pId3
                    Direction = 'Diagonal'

                if finalWinner == True:
                    
                    WINNER_EMBED = discord.Embed(
                        description = f"{fwc.upper()} just won!!! Congrats {fpId.mention}!",
                        title = f'GAME OVER!!! -> {Direction} win!',
                        color = discord.Color.green()
                    )

                    #WINNER_EMBED.set_image(url = fpId.avatar_url)
                    WINNER_EMBED.set_footer(text = 'I hope you enjoyed!!!')

                    await message.channel.send(embed = WINNER_EMBED)

                    OngoingGame = GAMES.get(message.author.id)
                    if OngoingGame==None: return
                    a = GAMES[message.author.id][0]
                    GAMES.pop(message.author.id)
                    GAMES.pop(a)
                    #await message.channel.send('Stopped :white_check_mark:')

client.run(TOKEN)
