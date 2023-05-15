import Crud
import math
import pandas as pd
import numpy as np
from detoxify import Detoxify

class Analyzer:
    def __init__(self):
        self.db = Crud.ChadbotDB()
        pass
    
    def calculate_emoji_sentiment(self, message):
        if len(message.reactions) == 0:
            return 0

        total_score = 0

        for reaction in message.reactions:
            emoji = self.db.fetch_emoji_by_id(reaction.emoji.id) \
                    if reaction.is_custom_emoji() \
                    else self.db.fetch_emoji_by_str(reaction.emoji)
            
            count = reaction.count
            score = emoji.sentiment_score if emoji else 0
            total_score += (score * math.log(count + 1, 2))
    
        return total_score / len(message.reactions)
    
    def predict_message_toxicity(self, message) -> dict:
        results = Detoxify('unbiased').predict(message)
        re_dict = {"is_toxic": False, "predictions": {}}
        for key, val in results.items():
            if val > 0.5:
                re_dict["predictions"][key] = True
                re_dict["is_toxic"] = True
            else:
                re_dict["predictions"][key] = False

        return re_dict


def main():
    pass
    # test code
    # analyzer = Analyzer()
    # results = analyzer.predict_message_toxicity("I will kill your mother")
    # for key, val in results["predictions"].items():
        
    # results = Detoxify('unbiased').predict(['Plot twist: I was the stabber'])
    # print(results)
    # df = pd.DataFrame(results)
    
    # # binary representation of true and false
    # df = (df > 0.5) * 1
    # print(df)

if __name__ == "__main__":
    main()
