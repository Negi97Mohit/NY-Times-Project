import streamlit as st
from pynytimes import NYTAPI
import streamlit as st
import pandas as pd


def main():

    api_key = "Frvpakmi7RzBNtGrwxKbcGNxwqBNvVEI"
    nyt = NYTAPI(api_key, parse_dates=True)

    movie_title = st.text_input("ENter the movie Name")

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


if __name__ == "__main__":
    st.title('NY Time Movies Review')
    main()
