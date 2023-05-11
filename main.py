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
	print(message.mentions, message.content)
	if client.user not in message.mentions:
		return

	await message.channel.send('You summoned me?')

client.run(os.getenv('TOKEN'))
# def main():
# 	''' main docstring '''

# if __name__ == "__main__":
# 	main()
