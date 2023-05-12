import discord
from discord.ext import commands
import dotenv
import os
import pandas as pd

dotenv.load_dotenv()

# Class with all the relevant info from a Discord.Message object
class Message:
	def __init__(self, id, content, author, created_at, guild, channel, attachments=None, embeds=None, reactions=None):
		self.id = id
		self.content = content
		self.author = author
		self.created_at = created_at
		self.guild = guild
		self.channel = channel
		self.attachments = attachments
		self.embeds = embeds
		self.reactions = reactions

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

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

	# Run commands with the message
	await client.process_commands(message)

	# Dar targeting code
	# if str(message.author) == "darr#1908":
	#     await message.add_reaction("<:dar:799348728632705064>")

@client.command(name='scan')
async def scan_command(ctx, channel_name: str):
	channel = discord.utils.get(ctx.guild.channels, name=channel_name)
	messageList = []
	if channel is None:
		await ctx.send(f"Cannot find channel {channel_name}")
		return

	try:
		async for message in channel.history(limit=100):
			reactions_info = []
			for reaction in message.reactions:
				reaction_info = {
					'emoji': str(reaction.emoji),
					'count': reaction.count
				}
				reactions_info.append(reaction_info)
			try:
				message_info = Message(
					id=message.id,
					content=message.content,
					author=str(message.author),
					created_at=message.created_at,
					guild=str(message.guild),
					channel=str(message.channel),
					attachments=[str(attachment.url) for attachment in message.attachments],
					embeds=[str(embed.to_dict()) for embed in message.embeds],
					reactions=reactions_info
				)
				messageList.append(message_info.__dict__)
			except Exception as error:
				print(f"Error creating Message object for message with id {message.id}: {error}")
	except Exception as error:
		print(f"Error retrieving history for channel {channel_name}: {error}")
		await ctx.send(f"Error retrieving history for channel {channel_name}")

	print(messageList) # This is where every message is stored
	await ctx.send(f"Scan completed for channel {channel_name}")

client.run(os.getenv('TOKEN'))
