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
    title = 'Join request - react with 👍 to accept.',
    color = discord.Color.dark_orange(),
    description = '{Player1} is requesting you, {Player2},  to join them for a game of Connect 4!!!'
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
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]: continue
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
    LastCoin = ''
    
    for i in range(0,7):
        for j in range(0,6):
            coin = Board[j][i]
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]: continue
            if LastCoin==coin[0]:
                counter[coin[0]] += 1
            LastCoin = coin[0]
            print('VERTICAL COUNTER:',counter)
            if counter.get(coin[0])!=None and counter.get(coin[0]) >= 3:
                return True, coin[0], await client.fetch_user(coin[1])
        LastCoin = ''
                

    return False, None, None

def getAt(Board, Row, CoinNumber):
    
    if Row < len(Board) and CoinNumber < len(Board[Row]):
        
        return Board[Row][CoinNumber]
    
    return None


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

    Uppercounter = {
        GAMES[message.author.id][2] : 0,
        GAMES[GAMES[message.author.id][0]][2] : 0
    }
    LowerCounter = {
        GAMES[message.author.id][2] : 0,
        GAMES[GAMES[message.author.id][0]][2] : 0
    }
    LastCoin = ''
    Direction = ''
    for i in range(7):
        for j in range(6):
            coin = getAt(Board, j, i)
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]: continue
            Uppercounter = LowerCounter = {GAMES[message.author.id][2] : 0,GAMES[GAMES[message.author.id][0]][2] : 0}

            for m in range(1,5):
                UpperCoin = getAt(Board, j - m, i + m)
                LowerCoin = getAt(Board, j + m, i + m)
                
                if UpperCoin!=None and UpperCoin[0] != GAMES[message.author.id][2] and UpperCoin[0] != GAMES[GAMES[message.author.id][0]][2]: UpperCoin = None
                if LowerCoin!=None and LowerCoin[0] != GAMES[message.author.id][2] and LowerCoin[0] != GAMES[GAMES[message.author.id][0]][2]: LowerCoin = None
                if UpperCoin == None and LowerCoin == None: continue
                if UpperCoin != coin and LowerCoin != coin: continue
                

                if UpperCoin != None:
                    Uppercounter[UpperCoin[0]]+=1
                
                if LowerCoin != None:
                    LowerCounter[LowerCoin[0]]+=1
                
                print(Uppercounter, LowerCounter, coin, LowerCoin, UpperCoin)
                
                if LowerCoin!=None and LowerCounter[LowerCoin[0]]>= 3:
                    print(LowerCounter[LowerCoin[0]])
                    return True, LowerCoin[0], await client.fetch_user(LowerCoin[1])
                elif UpperCoin!=None and Uppercounter[UpperCoin[0]]>=3:
                    print(Uppercounter[UpperCoin[0]])
                    return True, UpperCoin[0], await client.fetch_user(UpperCoin[1])

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

    if reaction.emoji == '👎':
        messageId = UPCOMING_GAME_REQUESTS.get(user.id)
        if messageId == None: return
        if reaction.message.id != messageId[0]: return
        UPCOMING_GAME_REQUESTS[user.id] = None
        await reaction.message.delete()

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
                
                a = JOIN_REQUEST_EMBED
                a.description = a.description.format(Player1 = message.author.name, Player2 = player.name)
                Join_request_message = await message.channel.send(embed = a)
                await message.channel.send(f'{player.name} React to the above message with 👍 to accept.')
                UPCOMING_GAME_REQUESTS[player.id] = [Join_request_message.id, message.author.id]

            if current_word == 'stop':
                OngoingGame = GAMES.get(message.author.id)
                if OngoingGame==None: return
                a = GAMES[message.author.id][0]
                GAMES[message.author.id] = None
                GAMES[a] = None
                await message.channel.send('Stopped :white_check_mark:')
            if current_word == 'help': await message.channel.send(embed=HELP_EMBED)
            if current_word == 'count': await message.channel.send(f"There are {len(GAMES)/2} game(s) being played right now!!!")
            if current_word == 'board':
                OngoingGame = GAMES.get(message.author.id)
                if OngoingGame==None: return
                Board = OngoingGame[1]
                final = getBoard(Board)
                await message.channel.send(embed = discord.Embed(title = 'Board',color = discord.Color.dark_red(), description = final).set_footer(text = 'type ,help for more info'))
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

                for i in range(len(Board)-1, 0, -1):
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
                    GAMES[message.author.id] = None
                    GAMES[a] = None
                    #await message.channel.send('Stopped :white_check_mark:')

client.run(TOKEN)
