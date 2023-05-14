import Crud
import math

class Rater:
    def __init__(self):
        self.db = Crud.ChadbotDB()
        pass
    
    def get_sentiment(self, message):
        total_score = 0

        for reaction in message.reactions:
            count = reaction.count

            score = self.db.fetch_by_emoji_id(reaction.emoji.id) \
                    if reaction.is_custom_emoji() \
                    else self.db.fetch_by_emoji(reaction.emoji)
            total_score += (score * math.log(count + 1, 2))
        
        return total_score / len(message.reactions)

def main():
    pass

if __name__ == "__main__":
    main()
