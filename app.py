import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Spotify API credentials
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")


# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load data
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to get album cover
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        return results["tracks"]["items"][0]["album"]["images"][0]["url"]
    return "https://i.postimg.cc/0QNxYz4V/social.png"  # Fallback image

# Function to recommend music
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    names, posters = [], []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        names.append(music.iloc[i[0]].song)
        posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
    return names, posters

# Streamlit UI
st.set_page_config(page_title="Music Recommender 🎵", layout="wide")

# Custom style
st.markdown(
    """
    <style>
        .main {
            background-color: #f9f9f9;
        }
        .css-18e3th9 {
            padding-top: 2rem;
        }
        .song-title {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🎧 Music Recommender App")
st.markdown("Get personalized music recommendations based on your favorite song. Powered by Spotify API and machine learning.")

# Sidebar
st.sidebar.header("Choose a Song")
music_list = music['song'].values
selected_song = st.sidebar.selectbox("Select a song you like:", music_list)

# Recommend button
if st.sidebar.button("Recommend"):
    st.markdown("---")
    st.markdown("## 🔥 Recommended Songs")
    names, posters = recommend(selected_song)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], width=150)
            st.markdown(f"<div class='song-title'>{names[i]}</div>", unsafe_allow_html=True)
