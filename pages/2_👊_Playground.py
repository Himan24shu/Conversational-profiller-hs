import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import helper
import preprocessor
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Conversational_profiler", page_icon=":bar_chart:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

WhatsApp_Animation= load_lottieurl("https://lottie.host/d5d4f84f-6de0-4b9c-8083-f88500da10dc/A5W74dRAQg.json")

st.title("Whatsapp Chat Analyzer")
with st.container():
    left_column, center_column,right_column = st.columns(3)
    with left_column:
        st.header("How to Extract Chat :book:")
        st.write(
            """
            - Open any of your what's App chat 
            - Click on Three dot at Right Top
            - Click on More
            - Click on Export Chat
            - Click on "Without Media"
            - Upload .txt File below
            - Phone users try to save .txt file in google drive than upload as whatsapp has stopped local storage for extracted chat.
            - PC users can upload file from there PC location after saving the chat.
            """

        )
    with right_column:
        st_lottie(WhatsApp_Animation, height=300, key="about")


hide_st_style= """
            <style>
            #MainMenu {visibilty:hidden;}
            footer{visibility:hidden;}
            </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.selectbox("Show analysis wrt", user_list)

    if st.button("Show Analysis"):

        num_msgs, words, num_media_msgs, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.subheader(num_msgs)

        with col2:
            st.subheader("Total Words")
            st.subheader(words)

        with col3:
            st.subheader("Media Shared")
            st.subheader(num_media_msgs)

        with col4:
            st.subheader("Links Shared")
            st.subheader(num_links)

        # timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(timeline['time'], timeline['message'], color='green', linestyle='--')
        plt.xticks(rotation='vertical',fontsize=12)
        st.pyplot(fig)

        st.title("Yearly Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
        plt.xticks(rotation='vertical',fontsize=12)
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation='vertical',fontsize=12)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical',fontsize=12)
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest user in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.fetch_most_busy_users(df)
            fig, ax = plt.subplots(figsize=(10, 6))

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical',fontsize=12)
                st.pyplot(fig)


            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical',fontsize=12)
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emojis  Analysis")
        try:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                plt.rcParams['font.sans-serif'] = 'Segoe UI Emoji'
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
        except:
            st.subheader(":smile: You don't have emoji in chat.")
