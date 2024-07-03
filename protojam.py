#Biblio
import streamlit as st
import pandas as pd
import base64
import requests


#Variables
df_music = pd.read_csv(r"C:\Users\eliot\Desktop\protojam\df_protojam.csv", sep=",")

#Fonctions
def sidebar_bg(side_bg):
   side_bg_ext = 'png'
   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

#système de recommandation
def reco(sport, genre=None):
    if genre:
        recommandation = df_music[(df_music['Sport'] == sport) & (df_music['genre'] == genre)].sort_values('popularity', ascending=False).sample(n=6, replace=True)
    else:
        recommandation = df_music[df_music['Sport'] == sport].sort_values('popularity', ascending=False).sample(n=6, replace=True)
    recommandation['link'] = recommandation['track_id'].apply(lambda x: f"https://open.spotify.com/track/{x}")
    return recommandation[['artist_name', 'track_name', 'link']]

def get_cover(link):
    oembed = f"https://open.spotify.com/oembed?url={link}"
    rep = requests.get(oembed)
    if rep.status_code == 200:
        data = rep.json()
        return data['thumbnail_url']
    else:
        return None

def main():
    side_bg = r"C:\Users\eliot\Desktop\protojam\background.png"
    sidebar_bg(side_bg)

    sport_choisi = st.sidebar.selectbox('Choisissez un sport', df_music['Sport'].unique())
    
    available_genres = df_music[df_music['Sport'] == sport_choisi]['genre'].unique()
    genre_choisi = st.sidebar.selectbox('Choisissez un genre', available_genres)

    if sport_choisi:
        st.title(f"Recommandation de musique pour {sport_choisi}:")
        recommandation = reco(sport_choisi, genre_choisi)

        cols = st.columns(3)

        for index, row in recommandation.iterrows():
            cover_url = get_cover(row['link'])
            with cols[index % 3]:
                if cover_url:
                    st.image(cover_url)
                st.markdown(f"[{row['track_name']}]({row['link']})")
                st.write(f"Artiste: {row['artist_name']}")

#Prog
if __name__ == '__main__':
    main()
