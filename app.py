import streamlit as st
import pickle
import pandas as pd
import requests

def recommend(song):
    song_index = songs[songs['song_title'] == song].index[0]
    distances = cosine[song_index]
    songs_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]

    recommended_music = []
    for i in songs_list:
        song_id = i[0]
        #fetch music from API
        recommended_music.append(songs.iloc[i[0]].song_title)
    return recommended_music

top_songs = pickle.load(open('songs_dict.pkl','rb'))
songs = pd.DataFrame(top_songs)

cosine = pickle.load(open('similarity.pkl','rb'))

st.title('TuneTeller - Music Recommender System')

selected_song_name = st.selectbox(
    'How would you like to be contacted?',
songs['song_title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_song_name)
    for i in recommendations:
        st.write(i)
