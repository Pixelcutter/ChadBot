import math
import models
from googleapiclient import discovery

class Analyzer:
    def __init__(self, db, api_key: str):
        self.db = db
        self.api_client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
            )
    
    def calculate_emoji_sentiment(self, reactions):
        if len(reactions) == 0:
            return 0

        total_score = 0

        for reaction in reactions:
            count = reaction.count
            emoji = self.db.fetch_emoji(reaction)            
            score = emoji.sentiment_score if emoji else 0
            total_score += (score * math.log(count + 1, 2))
    
        return total_score / len(reactions)
    
    def predict_message_toxicity(self, message: str, threshold: float = 0.75) -> models.ToxicReport:
        attributes = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "IDENTITY_ATTACK", "THREAT"]
        
        analyze_request = {
            'comment': { 'text': message },
            'languages': ["en"],
            'requestedAttributes': {attrib: { 'scoreThreshold': threshold } for attrib in attributes}
            }

        response = self.api_client.comments().analyze(body=analyze_request).execute()
        
        re_dict = {}
        for attrib in attributes:
            if "attributeScores" in response and attrib in response['attributeScores']:
                re_dict[attrib.lower()] = 1
            else:
                re_dict[attrib.lower()] = 0

        return models.ToxicReport(*re_dict.values())


def main():
    pass

if __name__ == "__main__":
    main()
