import discord

ERROR_EMBED = discord.Embed(
    title = 'Error',
    color = discord.Color.dark_gold(),
    description = 'No player mentioned. Please mention a player in order to play with them.\nExample: ,start @Connect-4'
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
    title = 'Help - How to play Connect 4 using Connect-4',
    description = 'The two players then alternate turns dropping one of their discs at a time into an unfilled column, until the second player, with red discs, achieves a four in a row, and wins the game.\n If the board fills up before either player achieves four in a row, then the game is a draw. \n\n\nType ,start @mention to start playing Connect 4 with someone. Use commands ,insert 1 to insert the coin into a specific row.\n',
    color = discord.Color.red()
)

HELP_EMBED.set_image(url = 'https://media.discordapp.net/attachments/762774251841257495/834002032561356810/unknown.png')
HELP_EMBED.set_footer(text='Type ,count to know how many players are playing the game right now!')
