import googleapiclient.discovery
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import re
# YouTube API credentials
api_key = 'Your- API- Key'


# Initialize emotion classifier
model_name = 'bhadresh-savani/bert-base-go-emotion'
model = AutoModelForSequenceClassification.from_pretrained(model_name, from_tf=False)
tokenizer = AutoTokenizer.from_pretrained(model_name)
emotion_classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

def detect_emotion(user_input):
    input_lower = user_input.lower()
    distress_keywords = ['suicidal', 'feeling down', 'depressed', 'hopeless', 'want to give up', 'not worth it', 'life is meaningless']
    for keyword in distress_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', input_lower):
            return 'suicidal'
    results = emotion_classifier(user_input)
    primary_emotion = results[0]['label']
    return primary_emotion

def map_emotion_to_query(emotion):
    if emotion in ['admiration', 'amusement', 'approval', 'joy', 'excitement', 'gratitude', 'love', 'relief', 'pride']:
        return 'happy songs'
    elif emotion in ['anger', 'annoyance', 'disapproval', 'disgust']:
        return 'angry songs'
    elif emotion in ['sadness', 'disappointment', 'grief', 'remorse', 'embarrassment', 'nervousness', 'fear', 'confusion']:
        return 'sad songs'
    else:
        return 'relaxing music'

def get_youtube_recommendations(query, language=None):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    if language and language.lower() != 'i am feeling lucky':
        query = f"{query} {language} songs"
    search_request = youtube.search().list(
        part="snippet",
        maxResults=20,
        q=query,
        type='video',
        videoDuration='medium',
        videoCategoryId='10'
    )
    search_response = search_request.execute()
    video_ids = [item['id']['videoId'] for item in search_response['items']]
    video_request = youtube.videos().list(
        part="snippet,statistics",
        id=','.join(video_ids)
    )
    video_response = video_request.execute()
    videos = sorted(video_response['items'], key=lambda x: int(x['statistics'].get('likeCount', 0)), reverse=True)
    top_videos = [f"{item['snippet']['title']} (https://www.youtube.com/watch?v={item['id']}) with {item['statistics'].get('likeCount', 0)} likes" for item in videos[:5]]
    return top_videos if top_videos else ["No recommendations available for this emotion and language"]
