"""
Module for the Chatbot handling conversational logic.
It uses Hugging Face's transformers to perform zero-shot classification for intent extraction.
"""

import os
import random
from transformers import pipeline
from .recommender import SongRecommender


class Chatbot:
    """
    A Chatbot that extracts user intents and provides conversational song recommendations.
    """

    def __init__(self):
        """
        Initializes the Chatbot by loading the recommendation engine and the zero-shot classifier.
        """
        self.recommender = SongRecommender()
        self.last_intent = None
        self.previously_recommended = []
        
        print("Loading local deep learning model (this may take a moment)...")
        # Use a zero-shot classifier to understand ANY text intent
        self.classifier = pipeline("zero-shot-classification", model="cross-encoder/nli-distilroberta-base")
        
        # We can map almost any user text to these labels
        self.candidate_labels = ["happy", "sad", "relaxed", "motivated", "pop", "rock", "hip-hop", "jazz", "classical", "world"]

    def extract_intent(self, text):
        """
        Extracts the mood or genre intent from the user's text.
        
        Args:
            text (str): The user's input text.
            
        Returns:
            str or None: The detected intent, 'different' for memory fallback, or None if confidence is low.
        """
        text_lower = text.lower()
        
        # Handle memory intent
        if any(word in text_lower for word in ["different", "more", "another", "else"]):
            return "different"
            
        # Predict intent using Deep Learning
        result = self.classifier(text, self.candidate_labels)
        best_intent = result['labels'][0]
        confidence = result['scores'][0]
        
        if confidence < 0.2:
            return None  # Not confident enough
            
        return best_intent
        
    def generate_conversational_intro(self, intent):
        """
        Generates a dynamic, non-rigid conversational response based on the intent.
        
        Args:
            intent (str): The detected mood or genre.
            
        Returns:
            str: A natural conversational preamble.
        """
        if intent == "happy":
            intros = [
                "I love that energy! Here's something upbeat to keep the good vibes going:\n\n",
                "Awesome! Let's match that great mood with some happy tracks:\n\n",
                "Glad to hear it! These songs should put a smile on your face:\n\n"
            ]
        elif intent == "sad":
            intros = [
                "I'm really sorry you're feeling down. Music always helps me. Try these:\n\n",
                "It's okay to feel sad sometimes. Here are some tracks that might comfort you:\n\n",
                "I hear you. Let me offer you some gentle songs for this moment:\n\n"
            ]
        elif intent == "relaxed":
            intros = [
                "Kick back and unwind! Here's some chill music for you:\n\n",
                "Nice and easy. These tracks are perfect for relaxing:\n\n",
                "Take a deep breath. Here are some smooth tunes to help you chill:\n\n"
            ]
        elif intent == "motivated":
            intros = [
                "Let's go! These high-energy tracks will get you moving:\n\n",
                "Time to crush it! Here are some bangers to keep you pumped:\n\n",
                "Feeling pumped? I've got just the right tracks for your adrenaline:\n\n"
            ]
        else:
            intros = [
                f"Oh, you want some {intent.capitalize()} music? I've got you covered:\n\n",
                f"Excellent choice. Let's dive into some great {intent.capitalize()} tracks:\n\n",
                f"I know exactly what you need. Here is some top-tier {intent.capitalize()} for you:\n\n"
            ]
                      
        return random.choice(intros)

    def get_response(self, user_message):
        """
        Processes the user message and returns a fully formatted bot response with recommendations.
        
        Args:
            user_message (str): The message typed by the user.
            
        Returns:
            str: The chatbot's reply.
        """
        intent = self.extract_intent(user_message)
        
        if intent == "different":
            if self.last_intent:
                intent = self.last_intent
                prefix = f"No problem at all! Let's try some totally different {intent} tracks this time:\n\n"
            else:
                return "I don't have anything to change up! Tell me what kind of mood or genre you're looking for first."
        else:
            if intent:
                self.last_intent = intent
                self.previously_recommended = []  # Reset memory
                prefix = self.generate_conversational_intro(intent)
            else:
                return "I'm a bit confused! Could you try phrasing that differently? You can tell me your mood or a genre you like."
            
        recommendations = self.recommender.recommend(intent=intent, exclude_songs=self.previously_recommended)
        
        if not recommendations:
            return f"I'm out of new {intent} songs right now! Please pick a different mood or genre."
            
        response = prefix
        for idx, song in enumerate(recommendations, 1):
            response += f"{idx}. **{song['Song_Name']}** by {song['Artist']} (Genre: {song['Genre']})\n"
            self.previously_recommended.append(song['Song_Name'])
            
        response += "\nLet me know if you want more recommendations or if you want to switch things up!"
        return response
