import streamlit as st
from pynytimes import NYTAPI


api_key = "Frvpakmi7RzBNtGrwxKbcGNxwqBNvVEI"
nyt = NYTAPI(api_key, parse_dates=True)

#App theme
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
#Grab the first data item in top_stories and view it

#Collecting top stories list
top_story = top_stories

#Getting list of section from the top story dictonary for creating the drop down menu.
section=set()
for ts in top_story:
    sec=str(ts["section"]).upper()
    section.add(sec)
    
option = st.selectbox(
    'Select the section Top Stories',
    (section))

#Getting the stories from certain section
stories=[]
for ts in top_story:
    sec=str(ts["section"]).upper()
    if sec==option:
        stories.append(ts)

#Getting list of stories title from the top story dictonary for creating the drop down menu.
title=[]
for ts in stories:
    titl=str(ts["title"]).upper()
    title.append(titl)

#Checkbox for the top stories title    
for titl in title:    
    st.checkbox(titl)

cols1,cols2=st.columns(2)

#storing the fiter values in ts_keys
ts_keys=[]
#getting the keys for the filter
for  key_val in stories[0].keys():
    ts_keys.append(key_val)
#removing the values of already existing keys value
ts_key_removed=['section','subsection','title']    
for elem in ts_key_removed:
    ts_keys.remove(elem)
        
with cols2:
    filter_val=st.multiselect("Select your filter",ts_keys)

with cols1:
    st.write(filter_val)



