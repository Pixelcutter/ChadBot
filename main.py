import discord
from discord.ext import commands
import dotenv
import os
import sqlite3
import SentimentAnalyzer
import ChadbotCRUD
import models

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
db = ChadbotCRUD.CRUD()
analyzer = SentimentAnalyzer.Analyzer(db=db, api_key=os.getenv("API_KEY"))

client = commands.Bot(command_prefix='!', intents=intents)

async def send_toxicity_report(message: discord.Message, toxic_report: models.ToxicReport):
	embed_var = discord.Embed(title="🚨 TOXIC COMMENT ALERT! 🚨", color=0xE31E33)
	embed_var.url = "https://www.verywellmind.com/mental-health-effects-of-reading-negative-comments-online-5090287"
	for field, val in toxic_report.__dict__.items():
		if val == True:
			embed_var.add_field(name=f"{field.replace('_', ' ').title()}  ✅", value="")
	await message.reply(embed=embed_var)


# dumb function that returns a fixed message based on rating
def get_rating_message(rating):
	msg = ""
	if rating >= -0.6 and rating <= 0.6:
		msg = "Average take..."
	elif rating < -0.6:
		if rating > -0.9:
			msg = "Bad take"
		else:
			msg = "Shit take. Consider deleting message"
	else:
		if rating < 0.9:
			msg = "Good take"
		else:
			msg = "God-tier take. Pin it"
	return msg

@client.event
async def on_ready():
	print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
	# print(message.author, message.mentions, message.content)
	if message.author == client.user:
		return

	# checks incoming messages for toxicity and prints a report if they are
	if message.content.startswith("!") == False:
		toxic_report = analyzer.predict_message_toxicity(message.content)
		print(toxic_report)
		if toxic_report.toxicity == True:
			await message.add_reaction("☣️")
			await db.save_message(message, toxic_report=toxic_report)
			# await send_toxicity_report(message, toxic_report)

	# Run commands with the message
	await client.process_commands(message)

# grabs server specific emojis and saves them to database table: emoji_sentiments
@client.command(name='emojis')
async def get_emojis(ctx):
	with sqlite3.connect("chadbot.db") as db:
		cursor = db.cursor()
		tuples = [(emoji.id, str(emoji), 0.0, emoji.name, ctx.guild.id, emoji.url) for emoji in ctx.guild.emojis]
		try:
			cursor.executemany('INSERT INTO emoji_sentiments (id, emoji, sentiment_score, name, guild_id, url) VALUES (?, ?, ?, ?, ?, ?)', tuples)
			db.commit()
		except discord.ext.commands.errors.CommandInvokeError:
			print(discord.ext.commands.errors.CommandInvokeError)


# command that rates a channel message thats been replied to by its reactions
@client.command(name='rate')
async def rate_command(ctx):
	ref = ctx.message.reference
	if ref == None:
		await ctx.send("There is nothing to rate...")
		return 
	
	original_msg = await ctx.fetch_message(ref.message_id)
	score = analyzer.calculate_emoji_sentiment(original_msg.reactions)
	await ctx.send(get_rating_message(score))

# Test function. Put whatever you want in here
@client.command(name="test")
async def test(ctx):
	toxic_report = models.ToxicReport()
	og = await ctx.fetch_message(ctx.message.reference.message_id)
	await db.save_message(og)
	

@client.command(name='scan')
async def scan_command(ctx, *channel_names):
	for channel_name in channel_names:
		channel = discord.utils.get(ctx.guild.channels, name=channel_name)
		if channel is None:
			await ctx.send(f"Cannot find channel {channel_name}")
			continue
		try:
			# NO LIMIT - WILL SAVE EVERY MESSAGE IN A CHANNEL
			async for message in channel.history(limit=None):
				await db.save_message(message)
		except Exception as error:
			print(f"Error retrieving history for channel {channel_name}: {error}")
			await ctx.send(f"Error retrieving history for channel {channel_name}")
	await ctx.send("Scan completed for all specified channels")

client.run(os.getenv('TOKEN'))
