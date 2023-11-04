import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

hide_st_style= """
            <style>
            #MainMenu {visibilty:hidden;}
            footer{visibility:hidden;}
            </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
img_lottie_animation = Image.open("images/yt_lottie_animation.png")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hi, I am Himanshu Sharma :wave:")
    st.title("A Software Engineer in this Technical World :wink:")
    st.write(
        "I am passionate about finding ways to Learn new stuffs to be more efficient and effective in Software Developers."
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
             :
            - I was student of Computer Application have pursued my Graduation in BCA
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
        st_lottie(lottie_coding, height=300, key="coding")

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
            - I was student of Computer Application have pursued my Graduation in BCA
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
