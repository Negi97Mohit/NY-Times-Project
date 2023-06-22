import streamlit as st
from pynytimes import NYTAPI
import streamlit as st
import pandas as pd
import movieposters as mp
import requests
from PIL import Image
from io import BytesIO
# library to extract movie ratings
from imdb import Cinemagoer
import imdb
import plotly.express as px

st.set_page_config(layout="wide")


def main():

    api_key = "Frvpakmi7RzBNtGrwxKbcGNxwqBNvVEI"
    nyt = NYTAPI(api_key, parse_dates=True)

    movie_title = st.text_input("ENter the movie Name")
    st.write("Searching for movie title with:", movie_title)
    reviews = nyt.movie_reviews(keyword=movie_title)
    # st.write(reviews)
    create_df(reviews)


def create_df(reviews):
    df_keys_temp = reviews[0].keys()
    df_keys = []
    for dic in df_keys_temp:
        df_keys.append(dic.capitalize())
    df_vals = []
    for dic in reviews:
        df_val_temp = []
        for val in dic.values():
            df_val_temp.append(val)
        df_vals.append(df_val_temp)

    movie_df = pd.DataFrame(df_vals, columns=df_keys)
    st.write(movie_df)

    create_list(movie_df, reviews)


def create_list(df, reviews):
    cols1, cols2 = st.columns(2)
    with cols1:
        title_list = df.Display_title.tolist()
        selected_title = st.multiselect("Select Movie Title", title_list)
        for sti in selected_title:
            link = mp.get_poster(title=sti)
            response = requests.get(link)
            img = Image.open(BytesIO(response.content))
            img = img.resize((300, 400))
            st.image(img)

    with cols2:
        st.title("Selected Movies")
        selcted_movies = df[df['Display_title'].isin(
            selected_title)].reset_index()
        st.write(selcted_movies)
        ia = Cinemagoer()
        im = imdb.IMDb()
        ratings = []
        # capturing the movie title imdb rating for movie review
        for title in selected_title:
            movies = ia.search_movie(title)
            sear = im.search_movie(title)
            id = sear[0].movieID
            mv = im.get_movie(id)
            # st.write(mv['directors'])
            rating = mv.data['rating']
            ratings.append(rating)
        fig = px.bar(ratings)
        st.plotly_chart(fig)


if __name__ == "__main__":
    st.title('NY Time Movies Review')
    main()
