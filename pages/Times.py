from nltk import sent_tokenize, word_tokenize
import datetime as dt
import numpy as np
from nltk.corpus import stopwords
import streamlit as st
from pynytimes import NYTAPI
import pandas as pd
from nltk.tokenize import word_tokenize as wt
from keybert import KeyBERT
from datetime import datetime


# Sentient analysis imports
import nltk
nltk.download('punkt')
nltk.download('wordnet')
# nlp = spacy.load("en_core_web_sm")

# S3 bucket cloud implementaion to be implementeds
# access_key_id = 'AKIASYW3E3PM3DD63GXN'
# secret_access_key = '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'
# bucket_name = 'times.sentiment.bucket'
# def get_s3():
#     s3 = boto3.resource('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
#     return s3

st.set_page_config(layout="wide")


def main():

    api_key = "Frvpakmi7RzBNtGrwxKbcGNxwqBNvVEI"
    nyt = NYTAPI(api_key, parse_dates=True)

    # App theme
    light = '''
    <style>
        "font-family:georgia;"
    </style>'''
    st.markdown(light, unsafe_allow_html=True)
    st.session_state.theme = "light"

    # Apply the theme to the app
    st.markdown(light, unsafe_allow_html=True)

    st.title("New York Times Stories Sentiment Analysis")

    top_stories = nyt.top_stories()
    # Grab the first data item in top_stories and view it

    # Collecting top stories list
    top_story = top_stories

    # Creating a table of all the top_stories
    # storing the keys for all the values
    ts_keys_main = []
    for keys in top_stories[0].keys():
        ts_keys_main.append(keys)
    # storing all the values as different line items
    values_keys = []
    for vals in top_stories:
        val_temp = []
        for values in vals.values():
            val_temp.append(values)
        values_keys.append(val_temp)
    # creating a dataframe for storing on cloud, in a s3 bucket
    story_df = pd.DataFrame(values_keys, columns=ts_keys_main)
    st.write(story_df)

    # Getting list of section from the top story dictonary for creating the drop down menu.
    section = set()
    for ts in top_story:
        sec = str(ts["section"])
        section.add(sec)
    option = st.selectbox(
        'Select the section Top Stories',
        (section))

    # Getting the stories from certain section
    stories = []
    for ts in top_story:
        sec = str(ts["section"])
        if sec == option:
            stories.append(ts)

    # Getting list of stories title from the top story dictonary for creating the drop down menu.
    title = []
    for ts in stories:
        titl = str(ts["title"])
        title.append(titl)

    # Checkbox for the top stories title
    selected_title = st.multiselect("select the story title", title)

    # storing the fiter values in ts_keys
    ts_keys = []
    # getting the keys for the filter
    for key_val in stories[0].keys():
        ts_keys.append(key_val)
    # removing the values of already existing keys value
    ts_key_removed = ['section', 'subsection', 'title', 'created_date']
    for elem in ts_key_removed:
        ts_keys.remove(elem)

    # storing the abstract for the stories
    abstract = []

    selected = str(option)
    selected = selected.lower()

    # colums for displaying the user filters and story content
    cols1, cols2 = st.columns(2)
    # cols2 contains the filter for the following dataframe
    with cols2:
        filter_val = st.multiselect("Select your filter", ts_keys)
    # cols1 displays the resultant dataframe with filters
    with cols1:
        # if the story title is not selected then it just filters
        if len(selected_title) == 0:
            if len(filter_val) == 0:
                filter_df = story_df.loc[story_df.section == selected]
                filter_df.drop(
                    columns=['title', 'subsection', 'section'], inplace=True)
                st.write(filter_df)
            else:
                filter_df = story_df.loc[story_df.section == selected]
                filter_df.drop(
                    columns=['title', 'subsection', 'section'], inplace=True)
                st.write(filter_df[filter_val])
                with st.expander("Stories"):
                    st.write(filter_df.abstract)
                    abstract = filter_df.abstract.tolist()
        # if story title is selected then it filters out based on the title
        else:
            if len(filter_val) == 0:
                filter_df = story_df.loc[story_df.section == selected]
                filter_df = story_df.loc[story_df['title'].isin(
                    selected_title)]
                filter_df.drop(
                    columns=['title', 'subsection', 'section'], inplace=True)
                st.write(filter_df)
            else:
                filter_df = story_df.loc[story_df.section == selected]
                filter_df = story_df.loc[story_df['title'].isin(
                    selected_title)]
                filter_df.drop(
                    columns=['title', 'subsection', 'section'], inplace=True)
                st.write(filter_df[filter_val])
        with st.expander("Stories"):
            st.write(filter_df.abstract)
            abstract = filter_df.abstract.tolist()
    st.write(abstract)
    kw_model = KeyBERT()
    keywords = filter_df.abstract.apply(kw_model.extract_keywords)

    # list of dates for the article
    dates = []
    dates_temp = filter_df.created_date.tolist()
    for dt in dates_temp:
        dates.append(datetime.date(dt))

    # list of keywords
    work_list = keywords.tolist()
    # storing the list of words
    words = []
    for word in work_list:
        w_temp = []
        for w in word:
            w_temp.append(w[0])
        words.append(w_temp)

    end_date = datetime.now()
    st.write(word)

    tweepy_file(word)

def tweepy_file(words):
    list_words=[]
    for word in words:
        list.append(word[0])
    st.write(list_words)
if __name__ == "__main__":
    main()
