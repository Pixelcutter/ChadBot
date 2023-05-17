import sqlite3
import discord
import models
from discord.ext import commands

# emojis from ayy lmao and chadbot sanctuary
# 0 = neutral
# negative < 0 > positive
sentiments = {
            "<:dar:799348728632705064>": -1,
            "<:maki:695456102506299404>": 0.6,
            "<:disgust:695462266916569198>": -0.8, 
            "<:gay:695468356232544286>": -0.9,
            "<:POG:700990278127058996>": 1,
            "<:POGCHAMP:703448221560733786>": 1,
            "<:fax:703448996688953465>": 0.7,
            "<:ayylmao:703449159918813225>": 0.4,
            "<:edog:706035531733270608>": 0.85,
            "<:fish1:708956998703775785>": -0.7,
            "<:kayli:737808766443192401>": 0.5,
            "<:bruh:737809957625266217>": -0.3,
            "<:ChonkerLimes:738358296372707350>": -0.15,
            "<:uwu:746297863956332584>": -0.4,
            "<:cry:758212295091945492>": -0.2,
            "<:megupog:762799018794680390>": 0.8,
            "<:whaat:779899808952614963>": -0.1,
            "<:IQ:804807567549267968>": 0.5,
            "<:dababy:823062117027938365>": 0.4,
            "<:ANGER:823063490804711436>": -0.8,
            "<:angrysad:823064712304394260>": -0.6,
            "<:feelsgood:823065821676961833>": 0.35,
            "<:feels:823066523996258304>": 0,
            "<:concernedface:823066956080873499>": -0.7,
            "<:sadblackguy:823069887819022359>": -0.2,
            "<:withered:829269120079888404>": -0.3,
            "<:gigachad:837896815780560906>": 1,
            "<:dislike:841981563214626817>": -1,
            "<:craigbliss:843142862484799508>": 0.7,
            "<:lukaspog:843348219617345548>": 0.9,
            "<:spence:845551713162625064>": -0.1,
            "<:makesyouthink:845552774669664257>": 0.1,
            "<:based:845896610701770783>": 0.8,
            "<:BustersVisage:871255968070131722>": -0.6, 
            "<:EngineerGaming:871256282336739429>": 0.2,
            "<:craigwojak:874317177380044840>": -0.5,
            "<:CringeHarold:874555282016075816>": -0.6,
            "<:cringe:874555774511247371>": -0.8,
            "<:ShinjiHand:874556278951784488>": -0.9,
            "<:Cummies:874556595785334815>": -0.9,
            "<:grim:904996831648428122>": -0.7,
            "<:kekw:914083965239963698>": 0.4,
            "<:rodmoment:975513940899557386>": -0.4,
            "<:blexbust:975566179601104947>": 0.6,
            "<:IMG_5301:976928817232883802>": -0.4,
            "<:blexbong:979285710198673459>": 0.3,
            "<:batemoji:983923908984045618>": -0.3,
            "<:wagmoney:1071512868996001852>": 0.5,
            "<:lol:1073450121204867082>": -1,
            "<:baby:1079137276707209307>": -0.6,
            "<:angry:1106868052664004649>": -0.7,
            "<:happy:1106868076554768475>": 0.7,
            "<:sad:1106868361482223636>": -0.3,
            "<:special:1106868830938091601>": 0.3,
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


class CRUD:
    def __init__(self):
        self.conn = sqlite3.connect("chadbot.db")
        self.cursor = self.conn.cursor()

    def fetch_emoji(self, reaction: discord.Reaction) -> models.Emoji:
        sql = f"SELECT * FROM emoji_sentiments WHERE id = '{reaction.emoji.id}'" \
              if reaction.is_custom_emoji() \
              else f"SELECT * FROM emoji_sentiments WHERE id = '{sum([ord(char) for char in reaction.emoji])}'"
        
        res = self.cursor.execute(sql).fetchone()
        return models.Emoji(*res) if res else None

    def save_emoji(self, reaction: discord.Reaction) -> bool:
        db_has_emoji = self.fetch_emoji(reaction)
        
        if db_has_emoji:
            return False
        
        emoji = reaction.emoji
        tup = (emoji.id, str(emoji), 0.0, emoji.name, reaction.message.guild.id, emoji.url) \
              if reaction.is_custom_emoji() \
              else (sum([ord(char) for char in emoji]), emoji, 0.0, "generic", 0, None)

        self.cursor.execute("""
                            INSERT INTO emoji_sentiments (id, emoji, sentiment_score, name, guild_id, url) 
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, tup)
        self.conn.commit()
        return True

    def fetch_user(self, user_id: int) -> models.User:
        sql = f"SELECT * FROM users WHERE id = '{user_id}'"        
        res = self.cursor.execute(sql).fetchone()
        return models.User(*res) if res else None

    def save_user(self, user: models.User, msg_count: int = 0, toxic_msg_count: int = 0, toxicity_score: int = 0) -> bool:
        db_has_user = self.fetch_user(user.id)

        if db_has_user:
            return False
        
        tup = (user.id, user.name, user.display_avatar, msg_count, toxic_msg_count, toxicity_score)
        self.cursor.execute("""
                            INSERT INTO users (id, name, display_avatar, msg_count, toxic_msg_count, toxicity_score) 
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, tup)
        self.conn.commit()
        return True

    def fetch_message(self, msg_id: int) -> models.Message:
        sql = f"SELECT * FROM messages WHERE id = '{msg_id}'"        
        res = self.cursor.execute(sql).fetchone()
        return models.Message(*res) if res else None

    def save_message(self, message: discord.Message, is_toxic: bool = False) -> bool:
        db_has_msg = self.fetch_message(message.id)

        if db_has_msg:
            return False
        
        tup = ( message.id, 
                message.author.id, 
                message.channel.id, 
                message.channel.guild.id, 
                message.content,
                message.created_at,
                message.jump_url,
                is_toxic )
        
        self.cursor.execute("""
                            INSERT INTO messages (id, author_id, channel_id, guild_id, text, created_at, jump_url, is_toxic) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, tup)
        self.conn.commit()
        return True

    

# only for testing
def main():
    pass
    # db = CRUD()
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