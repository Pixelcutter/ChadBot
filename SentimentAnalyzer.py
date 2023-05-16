import math
from googleapiclient import discovery

class Analyzer:
    def __init__(self, db, api_key: str, threshold: float):
        self.threshold = threshold
        self.db = db
        self.api_client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
            )
    
    def calculate_emoji_sentiment(self, message):
        if len(message.reactions) == 0:
            return 0

        total_score = 0

        for reaction in message.reactions:
            emoji = self.db.fetch_emoji(reaction)            
            count = reaction.count
            score = emoji.sentiment_score if emoji else 0
            total_score += (score * math.log(count + 1, 2))
    
        return total_score / len(message.reactions)
    
    def predict_message_toxicity(self, message) -> dict:
        attributes = {
            'TOXICITY': { 'scoreThreshold': self.threshold }, 
            'SEVERE_TOXICITY': { 'scoreThreshold': self.threshold }, 
            'INSULT': { 'scoreThreshold': self.threshold }, 
            'IDENTITY_ATTACK': { 'scoreThreshold': self.threshold }, 
            'THREAT': { 'scoreThreshold': self.threshold }
            }
        
        analyze_request = {
            'comment': { 'text': message },
            'languages': ["en"],
            'requestedAttributes': attributes
            }

        response = self.api_client.comments().analyze(body=analyze_request).execute()
        return response


def main():
    pass

if __name__ == "__main__":
    main()
