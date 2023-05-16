import ChadbotCRUD
import math
import pandas as pd
import numpy as np
from detoxify import Detoxify

class Rater:
    def __init__(self):
        self.db = ChadbotCRUD.CRUD()
        pass
    
    def calculate_message_score(self, message):
        total_score = 0

        for reaction in message.reactions:
            emoji = self.db.fetch_custom_emoji(reaction.emoji.id) \
                    if reaction.is_custom_emoji() \
                    else self.db.fetch_generic_emoji(reaction.emoji)
            
            count = reaction.count
            score = emoji.sentiment_score if emoji else 0
            total_score += (score * math.log(count + 1, 2))
        
        return total_score / len(message.reactions)

def main():
    results = Detoxify('unbiased').predict(['Plot twist: I was the stabber'])
    df = pd.DataFrame(results)
    
    # binary representation of true and false
    df = (df > 0.5) * 1
    print(df)

if __name__ == "__main__":
    main()
