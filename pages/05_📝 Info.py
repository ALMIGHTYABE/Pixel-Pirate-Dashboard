# Importing Libraries
import streamlit as st

# App
st.set_page_config(
    page_title="Info",
    page_icon="icons/pp.png",
    layout="wide",
)

# Title
st.title("📝 Info")

# Content
st.write("This web app is in beta. Will try to add more features and functions in the future.")
st.write("The address data is updated every 30 minutes. So if you have recently purchased a pp give it some time.")
st.write("The scores calculated are not official, I am not responsible for any losses incurred due to the same.")
st.write("The rarity scores is roughly calculated as follows:")
st.write(
    "[Rarity Score for a Trait Value] = 1 / ([Number of Items with that Trait Value] / [Total Number of Items in Collection])")
st.write("Additionally a bonus score is given to PPs that were 1/1s and specials.")
st.write("Stats Page includes data from all NFTs under the Hedgeys collection.")
