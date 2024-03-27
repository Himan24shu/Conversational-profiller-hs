import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image



#pageConfiguartion
st.set_page_config(
    page_title='Home Page',
    page_icon=':wave:',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items={
        'About': 'This App is developed by Himanshu Sharma to reach out please go in Contact section'
    }
)
hide_st_style= """
            <style>
            #MainMenu {visibilty:hidden;}
            footer{visibility:hidden;}
            </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
About_Animation= load_lottieurl("https://lottie.host/8bdd61b1-5a00-4422-bd6c-e5027963c766/FU1B036IlG.json")

img_lottie_animation = Image.open("images/yt_lottie_animation.png")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hi, I am Himanshu Sharma :wave:")
    st.title("A Software Engineer in this Technical World :wink:")
    st.write(
        "I am passionate about finding ways to Learn new stuffs."
    )
    #st.write("[Learn More >](https://pythonandvba.com)")



# ---- ABOUT THIS PROJECT ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("About this App")
        st.write("##")
        st.write(
            """
             The project basically analyze the WhatsApp chat:
            - This Project aims to develop a powerful and user-friendly application that provides valuable insights and statistical analysis from
            WhatsApp chat conversations. 
            - In today's digital age, messaging platforms like WhatsApp have become integral to our daily lives, serving as a primary means of communication for billions of
            users worldwide. 
            - By harnessing the vast amount of data generated through these conversations, this project seeks to empower users with a deeper understanding of their
            communication patterns, sentiment analysis, and content trends.
            
            Note : None of you data is getting stored in Any database, so feel free to use it.
            """
        )
    with right_column:
        st_lottie(About_Animation, height=300, key="about")

# ---- WHAT I DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What I do")
        st.write("##")
        st.write(
            """
            I am Software Engineer always eager to learn new stuffs, My Expertise :
            - I was student of Computer Application have pursued my Graduation in BCA and have completed my Masters from BITS Pillani.
            - Have completed my master in C
            - Working as a Software Engineer in WIPRO, leading team in ASP.NET
            - I have been experienced in Duck Creek technology(Finance tool).
            - Also my Expertise lies in SQl, Python, Streamlit, VB.Net, Duck Creek, ASP.net, HTML, CSS, JS

            If this sounds interesting to you, Do reach out to me for any Collaboration or Business related stuffs.
            """
        )
        st.header("Social Media handles")
        st.write("##")
        st.write("[Linkedin >](https://www.linkedin.com/in/himanshu-sharma-b80220155/)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="code")
