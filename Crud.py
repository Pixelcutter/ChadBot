import sqlite3
import discord
import models
from discord.ext import commands

# emojis from ayy lmao and chadbot sanctuary
# 0 = neutral
# negative < 0 > positive
sentiments = {
            "<:dar:799348728632705064>": -1,
            "<:maki:695456102506299404>": 1,
            "<:disgust:695462266916569198>": -1, 
            "<:gay:695468356232544286>": -1,
            "<:POG:700990278127058996>": 1,
            "<:POGCHAMP:703448221560733786>": 1,
            "<:fax:703448996688953465>": 1,
            "<:ayylmao:703449159918813225>": 1,
            "<:edog:706035531733270608>": 1,
            "<:fish1:708956998703775785>": 0,
            "<:kayli:737808766443192401>": 0,
            "<:bruh:737809957625266217>": -1,
            "<:ChonkerLimes:738358296372707350>": 1,
            "<:uwu:746297863956332584>": 1,
            "<:cry:758212295091945492>": -1,
            "<:megupog:762799018794680390>": 1,
            "<:whaat:779899808952614963>": -1,
            "<:IQ:804807567549267968>": 1,
            "<:dababy:823062117027938365>": 1,
            "<:ANGER:823063490804711436>": -1,
            "<:angrysad:823064712304394260>": -1,
            "<:feelsgood:823065821676961833>": 1,
            "<:feels:823066523996258304>": -1,
            "<:concernedface:823066956080873499>": -1,
            "<:sadblackguy:823069887819022359>": -1,
            "<:withered:829269120079888404>": -1,
            "<:gigachad:837896815780560906>": 1,
            "<:dislike:841981563214626817>": -1,
            "<:craigbliss:843142862484799508>": 1,
            "<:lukaspog:843348219617345548>": 1,
            "<:spence:845551713162625064>": 1,
            "<:makesyouthink:845552774669664257>": -1,
            "<:based:845896610701770783>": 1,
            "<:BustersVisage:871255968070131722>": -1, 
            "<:EngineerGaming:871256282336739429>": 0,
            "<:craigwojak:874317177380044840>": -1,
            "<:CringeHarold:874555282016075816>": -1,
            "<:cringe:874555774511247371>": -1,
            "<:ShinjiHand:874556278951784488>": 1,
            "<:Cummies:874556595785334815>": 1,
            "<:grim:904996831648428122>": -1,
            "<:kekw:914083965239963698>": 1,
            "<:rodmoment:975513940899557386>": -1,
            "<:blexbust:975566179601104947>": 1,
            "<:IMG_5301:976928817232883802>": -1,
            "<:blexbong:979285710198673459>": 1,
            "<:batemoji:983923908984045618>": -1,
            "<:wagmoney:1071512868996001852>": 1,
            "<:lol:1073450121204867082>": -1,
            "<:baby:1079137276707209307>": -1,
            "<:angry:1106868052664004649>": -1,
            "<:happy:1106868076554768475>": 1,
            "<:sad:1106868361482223636>": -1,
            "<:special:1106868830938091601>": 1,
        }

# updates hardcoded sentiments in db
# call this if you change the sentiment scores in the sentiments dict
def save_server_emoji_sentiments(db):
    sql = '''
            UPDATE emoji_sentiments
            SET sentiment_score = ?
            WHERE id = ?
          '''
    for emoji, score in sentiments.items():
        emoji_id = emoji.split(':')[-1][:-1]
        db.cursor.execute(sql, (score, emoji_id))

    db.conn.commit()


class ChadbotDB:
    def __init__(self):
        self.conn = sqlite3.connect("chadbot.db")
        self.cursor = self.conn.cursor()

    def fetch_emoji_by_str(self, emoji: str) -> models.Emoji:
        res = self.cursor.execute(f"SELECT * FROM emoji_sentiments WHERE emoji = '{emoji}'").fetchone()
        return models.Emoji(*res) if res else None

    def fetch_emoji_by_id(self, emoji_id: int) -> models.Emoji:
        res = self.cursor.execute(f"SELECT * FROM emoji_sentiments WHERE id = '{emoji_id}'").fetchone()
        return models.Emoji(*res) if res else None

    def save_reaction(self, reaction: discord.Reaction) -> bool:
        print(reaction)

    def save_message(self, ctx: commands.Context, message: discord.Message) -> bool:
        pass

    

# only for testing
def main():
    db = ChadbotDB()
    # call after manually changing sentiment scores in sentiments dict
    # save_server_emoji_sentiments(db)

    # db.cursor.execute("""CREATE TABLE IF NOT EXISTS guilds(
    #                      id INTEGER PRIMARY KEY, 
    #                      name TEXT
    #                      )"""
    #                  )
    # db.cursor.execute("""CREATE TABLE IF NOT EXISTS channels(
    #                      id INTEGER PRIMARY KEY, 
    #                      name TEXT, 
    #                      guild_id INTEGER
    #                      )"""
    #                  )
    # db.cursor.execute("""CREATE TABLE IF NOT EXISTS messages(
    #                      id INTEGER PRIMARY KEY, 
    #                      channel_id INTEGER, 
    #                      content TEXT, 
    #                      created_at TEXT, 
    #                      emoji_sentiment REAL
    #                      )"""
    #                  )
    # db.cursor.execute("""CREATE TABLE IF NOT EXISTS reactions(
    #                      id INTEGER PRIMARY KEY AUTOINCREMENT, 
    #                      message_id INTEGER, 
    #                      emoji TEXT, 
    #                      count INTEGER
    #                      )"""
    #                  )
    # db.conn.commit()
    # db.conn.close()


if __name__ == "__main__":
    main()