# 🎵 Music Recommendation App

A Python-based music recommendation system powered by Spotify's API. This app provides intelligent song recommendations based on user preferences, using machine learning for similarity comparison and Streamlit for a sleek, interactive user interface.

---

## 🚀 Features

- 🎧 **Smart Music Recommendations**: Suggests songs based on the user's selected genre or artist.
- 🎨 **Visual Experience**: Displays album covers alongside each recommended track.
- 🔗 **Spotify API Integration**: Leverages Spotify's search and metadata capabilities.
- 🖥️ **Web Interface**: Built using [Streamlit](https://streamlit.io/) for ease of use and real-time interaction.

---

## 🧰 Requirements

Before getting started, ensure you have the following:

- **Python** ≥ 3.6
- A **Spotify Developer account** with API credentials (Client ID and Client Secret)

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

# ⚙️ Setup
Follow these steps to get the project running on your local machine:

## 1. Clone the Repository

```bash
https://github.com/mrablfz05/recommendation-ml-system.git
```
Replace your-username with your actual GitHub username if you’re cloning your own fork.

## 2. Navigate to the Project Directory

```bash
cd ml-python
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all the required libraries including:

> spotipy (for Spotify API interaction).
> streamlit (for the app UI).
> pandas, scikit-learn, etc. (for data handling and ML).

# 🔐 Spotify API Credentials Setup
To use Spotify's API, you need to create a developer account and set up authentication credentials.

## 📥 Step-by-step:

> - 1.Go to the Spotify Developer Dashboard.
> - 2.Log in with your Spotify account.
> - 3.Click Create an App.
> - 4.Give your app a name and description, then click Create.
> - 5.After the app is created, you'll see:

- Client ID
- Client Secret

## 🛠️ Set Environment Variables

```bash
setx SPOTIPY_CLIENT_ID "your-client-id"
setx SPOTIPY_CLIENT_SECRET "your-client-secret"
setx SPOTIPY_REDIRECT_URI "http://localhost:8888/callback"
```

## ▶️ Running the App

```bash
streamlit run app.py
```