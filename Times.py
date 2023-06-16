import streamlit as st
from pynytimes import NYTAPI
import pandas as pd
import boto3


#S3 bucket cloud implementaion to be implementeds
# access_key_id = 'AKIASYW3E3PM3DD63GXN'
# secret_access_key = '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'
# bucket_name = 'times.sentiment.bucket'
# def get_s3():
#     s3 = boto3.resource('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)  
#     return s3

def main():

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

    #Creating a table of all the top_stories
    #storing the keys for all the values 
    ts_keys_main=[]
    for keys in top_stories[0].keys():
        ts_keys_main.append(keys)
    #storing all the values as different line items
    values_keys=[]
    for vals in top_stories:
        val_temp=[]
        for values in vals.values():
            val_temp.append(values)
        values_keys.append(val_temp)
    #creating a dataframe for storing on cloud, in a s3 bucket
    story_df=pd.DataFrame(values_keys,columns=ts_keys_main)
    st.write(story_df)

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

    #storing the fiter values in ts_keys
    ts_keys=[]
    #getting the keys for the filter
    for  key_val in stories[0].keys():
        ts_keys.append(key_val)
    #removing the values of already existing keys value
    ts_key_removed=['section','subsection','title']    
    for elem in ts_key_removed:
        ts_keys.remove(elem)
            
    selected=str(option)
    selected=selected.lower()
    st.write(selected)

    #colums for displaying the user filters and story content
    cols1,cols2=st.columns(2)
    #cols2 contains the filter for the following dataframe
    with cols2:
        filter_val=st.multiselect("Select your filter",ts_keys)
    #cols1 displays the resultant dataframe with filters
    with cols1:
        if len(filter_val)==0:
            filter_df=story_df.loc[story_df.section==selected]
            filter_df.drop(columns=['title','subsection','section'],inplace=True)
            st.write(filter_df)
        else:
            filter_df=story_df.loc[story_df.section==selected]
            filter_df.drop(columns=['title','subsection','section'],inplace=True)
            st.write(filter_df[filter_val])
            return_filter(filter_df)
            
def return_filter(filter_vals):
    return filter_vals

if __name__=="__main__":
    main()
