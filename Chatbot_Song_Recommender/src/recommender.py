"""
Module for the SongRecommender engine.
Handles dataset loading, filtering, and recommending songs based on extracted audio features.
"""

import os
import pandas as pd


class SongRecommender:
    """
    A class that recommends songs based on mood (valence/energy) or genre.
    """

    def __init__(self, data_path=None):
        """
        Initializes the SongRecommender by loading the dataset.
        
        Args:
            data_path (str, optional): Custom path to the dataset CSV. Defaults to 'data/SpotifyFeatures.csv'.
        """
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, 'data', 'SpotifyFeatures.csv')
        
        self.df = pd.read_csv(data_path)
        # Drop duplicates based on track_name and artist_name
        self.df = self.df.drop_duplicates(subset=['track_name', 'artist_name'])
        # Filter for somewhat popular songs to avoid obscure tracks
        self.df = self.df[self.df['popularity'] >= 40]
    
    def recommend(self, intent=None, num_recommendations=3, exclude_songs=None):
        """
        Recommend songs based on intent (mood or genre), excluding previously recommended songs.
        
        Args:
            intent (str): The detected mood or genre.
            num_recommendations (int): Number of songs to return.
            exclude_songs (list): List of song names to avoid recommending again.
            
        Returns:
            list: A list of dictionaries containing Song_Name, Artist, and Genre.
        """
        if exclude_songs is None:
            exclude_songs = []
            
        filtered_df = self.df.copy()
        
        if exclude_songs:
            filtered_df = filtered_df[~filtered_df['track_name'].isin(exclude_songs)]
            
        if intent:
            intent = intent.lower()
            if intent == "happy":
                filtered_df = filtered_df[(filtered_df['valence'] >= 0.6) & (filtered_df['energy'] >= 0.6)]
            elif intent == "sad":
                filtered_df = filtered_df[(filtered_df['valence'] <= 0.4) & (filtered_df['energy'] <= 0.5)]
            elif intent == "relaxed":
                filtered_df = filtered_df[(filtered_df['energy'] <= 0.5) & (filtered_df['valence'] > 0.3)]
            elif intent == "motivated":
                filtered_df = filtered_df[filtered_df['energy'] >= 0.75]
            else:
                # It's probably a genre
                filtered_df = filtered_df[filtered_df['genre'].str.lower() == intent]
                
        if filtered_df.empty:
            # Fallback
            filtered_df = self.df
            if exclude_songs:
                filtered_df = filtered_df[~filtered_df['track_name'].isin(exclude_songs)]
            
        # Select n random songs
        if len(filtered_df) > num_recommendations:
            recommendations = filtered_df.sample(num_recommendations)
        else:
            recommendations = filtered_df
            
        # Format output
        results = []
        for _, row in recommendations.iterrows():
            results.append({
                'Song_Name': row['track_name'],
                'Artist': row['artist_name'],
                'Genre': row['genre']
            })
            
        return results
