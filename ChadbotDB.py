import sqlite3
import discord
from discord.ext import commands

class ChadbotDB:
    def __init__(self):
        self.conn = sqlite3.connect("chadbot.db")
        self.cursor = self.conn.cursor()

    def save_reaction(self, reaction: discord.Reaction) -> bool:
        print(reaction)

    def save_message(self, ctx: commands.Context, message: discord.Message) -> bool:
        pass

    

# only for testing
def main():
    db = ChadbotDB()
    db.save_reaction("some reaction")
    db.cursor.execute("""CREATE TABLE IF NOT EXISTS guilds(
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT
                         )"""
                     )
    db.cursor.execute("""CREATE TABLE IF NOT EXISTS channels(
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         name TEXT, 
                         guild_id INTEGER
                         )"""
                     )
    db.cursor.execute("""CREATE TABLE IF NOT EXISTS messages(
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         channel_id INTEGER, 
                         content TEXT, 
                         created_at TEXT, 
                         sentiment INTEGER
                         )"""
                     )
    db.cursor.execute("""CREATE TABLE IF NOT EXISTS reactions(
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         message_id INTEGER, 
                         emoji TEXT, 
                         count INTEGER
                         )"""
                     )
    db.cursor.execute("""CREATE TABLE IF NOT EXISTS guild_emojis(
                         guild_id INTEGER, 
                         emoji TEXT, 
                         sentiment INTEGER
                         )"""
                     )
    db.cursor.execute("""CREATE TABLE IF NOT EXISTS generic_emojis(
                         emoji TEXT, 
                         sentiment INTEGER
                         )"""
                     )
    db.conn.commit()
    db.conn.close()


if __name__ == "__main__":
    main()