import discord
import database
import commands
import ast

def getBoard(Board, user = None):
    final = ''
    #print(Board)

    for i in Board:
        a = i
        for j in a:
            final += f':{j[0]}_circle:'
        final += '\n'
    return final

def checkDirection(Board, Row, CoinNumber, RowIncr, CoinIncr):
    coin = getAt(Board, Row, CoinNumber)

    counter = 0
    currentCoin, CurrentRow, CurrentCoinNumber = coin,Row,CoinNumber
    
    while counter<4:
        #print(currentCoin, CurrentRow, CurrentCoinNumber, counter)
        if currentCoin != None and currentCoin == coin:
            counter += 1
        else:
            return False, []
        
        CurrentCoinNumber+= CoinIncr
        CurrentRow += RowIncr
        currentCoin = getAt(Board, CurrentRow, CurrentCoinNumber)
    #print(counter)
    return True, [counter, CurrentCoinNumber, CurrentRow, CoinNumber, Row, RowIncr, CoinIncr]

def checkHorizontal(Board, message, GAMES, client):
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
    HorizontalCheck, counter = False, []
    for i in range(6):
        for j in range(7):
            coin = getAt(Board, i, j)
            if coin == None: break
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]: continue
            
            HorizontalCheck, counter = checkDirection(Board, i, j, 0, 1)
            if HorizontalCheck == True: return True, coin[0], counter

    return False, None, counter

def checkVertical(Board, message, GAMES, client):
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
    VerticalCheck, counter = False, []
    for i in range(0,7):
        for j in range(0,6):
            coin = getAt(Board, j, i)
            if coin == None: break
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]: continue
            
            VerticalCheck, counter = checkDirection(Board, j, i, 1, 0)

            if VerticalCheck == True: return True, coin[0], counter
        
                

    return False, None, counter

def getAt(Board, Row, CoinNumber):
    
    if Row < len(Board) and CoinNumber < len(Board[Row]) and Row>=0 and CoinNumber>=0:
        
        return Board[Row][CoinNumber]
    
    return None

def checkDiagonal(Board, message, GAMES, client):
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

    UpperCheck, LowerCheck, counter1, counter2 = False, False, [], []
    for i in range(7):
        for j in range(6):
            coin = getAt(Board, j, i)
            if coin == None: break
            if coin[0] != GAMES[message.author.id][2] and coin[0] != GAMES[GAMES[message.author.id][0]][2]: continue

            UpperCheck, counter1 = checkDirection(Board, j, i, -1, 1)
            LowerCheck, counter2 = checkDirection(Board, j, i, 1, 1)

            #print(UpperCheck, LowerCheck)
            
            if LowerCheck==True or UpperCheck == True:
                return True, coin[0], counter1, counter2

    return False, None, counter1, counter2


def getWinningBoard(Board, a):
    Row = a[4]
    CoinNumber = a[3]
    CoinIncr = a[6]
    RowIncr = a[5]

    counter = 0
    CurrentRow, CurrentCoinNumber = Row,CoinNumber

    while counter<4:
        #print('EEEE:',currentCoin, CurrentRow, CurrentCoinNumber, counter)
        
        #print('BOARD:', Board)
        #print(CurrentRow, CurrentCoinNumber, getAt(Board, CurrentRow, CurrentCoinNumber))
        Board[CurrentRow][CurrentCoinNumber][0] = 'purple'

        CurrentCoinNumber+= CoinIncr
        CurrentRow += RowIncr

        counter += 1

async def checkWinner(GAMES, message, client):

    OngoingGame = GAMES.get(message.author.id)
    if OngoingGame==None: return
    Board = OngoingGame[1]

    h, hwc, c1 = checkHorizontal(Board, message, GAMES, client)
    v, vwc, c2 = False, None, []
    d, dwc, c3, c4 = False, None, [], []
    if h == False:
        v, vwc, c2 = checkVertical(Board, message, GAMES, client)
    if h==False and v==False:
        d, dwc, c3, c4 = checkDiagonal(Board, message, GAMES, client)
    
    finalWinner, fwc, fpId, fc1, fc2 = False, None, None, None, None
    Direction = ''
    pId1 = pId2 = pId3 = message.author
    if h==True:
        finalWinner, fwc, fpId, fc1 = h, hwc, pId1, c1
        Direction = 'Horizontal'
    elif v==True:
        finalWinner, fwc, fpId, fc1 = v, vwc, pId2, c2
        Direction = 'Vertical'
    elif d==True:
        finalWinner, fwc, fpId, fc1, fc2 = d, dwc, pId3, c3, c4
        Direction = 'Diagonal'

    if finalWinner == True:
        
        WINNER_EMBED = discord.Embed(
            description = f"{fwc.upper()} just won!!! Congrats {fpId.mention}!",
            title = f'GAME OVER!!! -> {Direction} win!',
            color = discord.Color.green()
        )

        #WINNER_EMBED.set_image(url = fpId.avatar_url)
        WINNER_EMBED.set_footer(text = 'I hope you enjoyed!!!')

        OngoingGame = GAMES.get(message.author.id)
        if OngoingGame==None: return
        await commands.stop(GAMES, message, False)

        #await message.channel.send('Stopped :white_check_mark:')

        db1 = database.database()
        db1.createTable()
        Data = db1.getData(fpId.id)
        Data = Data or [0,0]

        try: int(Data[1])
        except: Data[1] = 0
        
        a='saved'
        if Data!=None:
            a=db1.saveData(fpId.id, str(int(Data[1])+500))
            print(db1.getData(fpId))
        else:
            a=db1.saveData(fpId.id, '500')
        #await message.channel.send(f'{a} Data for {fpId.mention}')

        if Direction == 'Diagonal':
            a = fc2
            if len(fc1)>0:
                a = fc1

        else:
            a = fc1

        getWinningBoard(Board, a)
        await message.channel.send(embed = WINNER_EMBED)
        OtherPlayer = await client.fetch_user(OngoingGame[0])

        await commands.saveboard({'Name':OtherPlayer.name, 'Id':OtherPlayer.id}, Board, {'Name':message.author.name, 'Id':message.author.id})
        await message.channel.send(embed = discord.Embed(title = f"{message.author.name} WON!!!",color = (fwc=='red' and discord.Color.dark_red() or discord.Color.dark_blue()), description = getBoard(Board)).set_footer(text = 'type ,help for more info'))

        