import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load data
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Language translations
translations = {
    "en": {
        "title": "🎧 Music Recommender App",
        "description": "Get personalized music recommendations based on your favorite song. Powered by Spotify API and machine learning.",
        "sidebar_title": "Choose a Song",
        "sidebar_select": "Select a song you like:",
        "recommend_button": "Recommend",
        "recommended_title": "🔥 Recommended Songs",
        "language": "Language"
    },
    "fa": {
        "title": "🎧 سامانه پیشنهاد آهنگ",
        "description": "پیشنهادهای شخصی‌سازی‌شده بر اساس آهنگ مورد علاقه شما. با استفاده از اسپاتیفای و یادگیری ماشین.",
        "sidebar_title": "آهنگ مورد علاقه را انتخاب کنید",
        "sidebar_select": "آهنگی را انتخاب کنید:",
        "recommend_button": "پیشنهاد بده",
        "recommended_title": "🔥 آهنگ‌های پیشنهادی",
        "language": "زبان"
    }
}

# Set page config
st.set_page_config(page_title="Music Recommender 🎵", layout="wide")

# Language selector
lang = st.sidebar.radio(
    label=translations["en"]["language"],
    options=["en", "fa"],
    format_func=lambda x: "English" if x == "en" else "فارسی"
)
t = translations[lang]

# Custom style
st.markdown(
    """
    <style>
        .main {
            background-color: #f9f9f9;
        }
        .song-title {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
        }
        .stRadio > div {
            flex-direction: row;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title(t["title"])
st.markdown(t["description"])

# Sidebar UI
st.sidebar.header(t["sidebar_title"])
selected_song = st.sidebar.selectbox(t["sidebar_select"], music['song'].values)

# Get album cover URL
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    try:
        results = sp.search(q=search_query, type="track")
        if results and results["tracks"]["items"]:
            return results["tracks"]["items"][0]["album"]["images"][0]["url"]
    except Exception as e:
        print(f"Spotify API error: {e}")
    return "https://i.postimg.cc/0QNxYz4V/social.png"  # Default fallback image

# Recommendation logic with randomness
def recommend(song):
    # Get index of the selected song
    index = music[music['song'] == song].index[0]

    # Sort the songs based on similarity
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    # Get the top 10 closest songs, including the selected song (so we don't suggest it again)
    top_similar_songs = distances[1:11]

    # Shuffle the top 10 songs to ensure randomness
    random.shuffle(top_similar_songs)

    names, posters = [], []

    # Select the top 5 after shuffling for recommendation
    for i in top_similar_songs[:5]:
        artist = music.iloc[i[0]].artist
        names.append(music.iloc[i[0]].song)
        posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))

    return names, posters

# Display recommendations
if st.sidebar.button(t["recommend_button"]):
    st.markdown("---")
    st.markdown(f"## {t['recommended_title']}")
    names, posters = recommend(selected_song)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], width=150)
            st.markdown(f"<div class='song-title'>{names[i]}</div>", unsafe_allow_html=True)
