key = "..."
endpoint = "..."

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticateClient():
    credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=credential)
    return text_analytics_client

def sentiment():
    
    client = authenticateClient()

    try:
        documents = [
            {"id": "1", "language": "en", "text": "I had the best day of my life."},
            {"id": "2", "language": "en",
                "text": "This was a waste of my time. The speaker put me to sleep."},
            {"id": "3", "language": "es", "text": "No tengo dinero ni nada que dar..."},
            {"id": "4", "language": "tur",
                "text": "aldım gayet başarılı"}
        ]

        response = client.analyze_sentiment(documents=documents)
        for document in response:
            print("Document Id: ", document.id, ", Sentiment: ", document.sentiment)
            score = document.confidence_scores
            print("\tConfidence Scores: ")
            print("\t\tNegative: {:.2f}\tNeutral: {:.2f}\tPositive: {:.2f}"
                  .format(score.negative, score.neutral, score.positive))

    except Exception as err:
        print("Encountered exception. {}".format(err))
sentiment()

def language_detection_example(client):
    try:
        documents = ["Ce document est rédigé en Français."]
        response = client.detect_language(documents = documents, country_hint = 'us')[0]
        print("Language: ", response.primary_language.name)

    except Exception as err:
        print("Encountered exception. {}".format(err))
language_detection_example(client)