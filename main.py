import discord
import dotenv
import os

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
	print(message)
	print(message.author, message.mentions, message.content)

	if message.author == client.user:
		return
	
	if client.user in message.mentions:
		await message.channel.send('sup?')

	# Dar targeting code
	# if str(message.author) == "darr#1908":
	# 	await message.add_reaction("<:dar:799348728632705064>")

client.run(os.getenv('TOKEN'))