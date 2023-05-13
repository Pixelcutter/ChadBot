class Rater:
    def __init__(self):
        # some default emojis and emojis from ayy lmao and chadbot sanctuary
        # 0 = neutral
        # -1 = negative, -2 = very negative, -3 = dar
        # 1 = positive, 2 = very positive
        self.sentiments = {
            "<:dar:799348728632705064>": -3,
            "<:maki:695456102506299404>": 1,
            "<:disgust:695462266916569198>": -2, 
            "<:gay:695468356232544286>": -2,
            "<:POG:700990278127058996>": 2,
            "<:POGCHAMP:703448221560733786>": 2,
            "<:fax:703448996688953465>": 1,
            "<:ayylmao:703449159918813225>": 2,
            "<:edog:706035531733270608>": 1,
            "<:fish1:708956998703775785>": 0,
            "<:kayli:737808766443192401>": 0,
            "<:bruh:737809957625266217>": -2,
            "<:ChonkerLimes:738358296372707350>": 1,
            "<:uwu:746297863956332584>": 1,
            "<:cry:758212295091945492>": -1,
            "<:megupog:762799018794680390>": 2,
            "<:whaat:779899808952614963>": -1,
            "<:IQ:804807567549267968>": 1,
            "<:dababy:823062117027938365>": 1,
            "<:ANGER:823063490804711436>": -2,
            "<:angrysad:823064712304394260>": -1,
            "<:feelsgood:823065821676961833>": 1,
            "<:feels:823066523996258304>": -1,
            "<:concernedface:823066956080873499>": -1,
            "<:sadblackguy:823069887819022359>": -1,
            "<:withered:829269120079888404>": -2,
            "<:gigachad:837896815780560906>": 2,
            "<:dislike:841981563214626817>": -2,
            "<:craigbliss:843142862484799508>": 2,
            "<:lukaspog:843348219617345548>": 2,
            "<:spence:845551713162625064>": 2,
            "<:makesyouthink:845552774669664257>": -1,
            "<:based:845896610701770783>": 1,
            "<:BustersVisage:871255968070131722>": -2, 
            "<:EngineerGaming:871256282336739429>": 0,
            "<:craigwojak:874317177380044840>": -1,
            "<:CringeHarold:874555282016075816>": -2,
            "<:cringe:874555774511247371>": -2,
            "<:ShinjiHand:874556278951784488>": 1,
            "<:Cummies:874556595785334815>": 2,
            "<:grim:904996831648428122>": -2,
            "<:kekw:914083965239963698>": 2,
            "<:rodmoment:975513940899557386>": -1,
            "<:blexbust:975566179601104947>": 2,
            "<:IMG_5301:976928817232883802>": -1,
            "<:blexbong:979285710198673459>": 1,
            "<:batemoji:983923908984045618>": -2,
            "<:wagmoney:1071512868996001852>": 1,
            "<:lol:1073450121204867082>": -2,
            "<:baby:1079137276707209307>": -1,
            "<:angry:1106868052664004649>": -3,
            "<:happy:1106868076554768475>": 2,
            "<:sad:1106868361482223636>": -2,
            "<:special:1106868830938091601>": 3,
            "🔥": 2,
            "👍": 1,
            "😂": 2,
            "😡": -2,
            "😠": -1,
            "😀": 1,
            "😍": 2,
            "👎": -1,
            "💯": 2,
            "💀": -1,
        }
    
    def get_sentiment(self, message):
        total_score = 0

        for reaction in message.reactions:
            if str(reaction.emoji) not in self.sentiments:
                print("skipping", str(reaction.emoji))
                continue

            count = reaction.count if reaction.is_custom_emoji() else 1
            total_score += (self.sentiments[str(reaction.emoji)] * count)
        
        return total_score

def main():
    pass

if __name__ == "__main__":
    main()