import time

import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # data web app development
import yaml
from PIL import Image

# App
st.set_page_config(
    page_title="Pixel Pirate Tracker",
    page_icon="icons/pp.png",
    layout="wide",
)

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Read Data
dataset_url = config["main"]["data-source"]


@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


df = get_data()
nft_df = get_data()

# Dashboard Title
st.title("Pixel Pirate Tracker")
# st.markdown("# Pixel Pirate Tracker️")
st.sidebar.markdown("# Pixel Pirate Tracker️")

# Top-Level Filters
address_filter = st.multiselect("Select your address", pd.unique(df["address"]))

# Sidebar - title & filters
batch = pd.unique(df["Batch"])
type = pd.unique(df["Type"])
background = pd.unique(df["Background"])
base = pd.unique(df["Base"])
outfit = pd.unique(df["Outfit"])
necklace = pd.unique(df["Necklace"])
eye = pd.unique(df["Eye"])
beard = pd.unique(df["Beard"])
hair = pd.unique(df["Hair"])
hat = pd.unique(df["Hat"])
hand = pd.unique(df["Hand_Accessories"])
shoulder = pd.unique(df["Shoulder"])
mouth = pd.unique(df["Mouth"])

st.sidebar.markdown('### Data Filters')
batch_choice = st.sidebar.multiselect(
    'Choose batch:', batch, default=batch)
type_choice = st.sidebar.multiselect(
    'Choose type:', type, default=type)
background_choice = st.sidebar.multiselect(
    'Choose background:', background, default=background)
base_choice = st.sidebar.multiselect(
    'Choose base:', base, default=base)
outfit_choice = st.sidebar.multiselect(
    'Choose outfit:', outfit, default=outfit)
necklace_choice = st.sidebar.multiselect(
    'Choose necklace:', necklace, default=necklace)
eye_choice = st.sidebar.multiselect(
    'Choose eye:', eye, default=eye)
beard_choice = st.sidebar.multiselect(
    'Choose beard:', beard, default=beard)
hair_choice = st.sidebar.multiselect(
    'Choose hair:', hair, default=hair)
hat_choice = st.sidebar.multiselect(
    'Choose hat:', hat, default=hat)
hand_choice = st.sidebar.multiselect(
    'Choose hand:', hand, default=hand)
shoulder_choice = st.sidebar.multiselect(
    'Choose shoulder:', shoulder, default=shoulder)
mouth_choice = st.sidebar.multiselect(
    'Choose mouth:', mouth, default=mouth)

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["address"].isin(address_filter)]
df = df[df["Batch"].isin(batch_choice)]
df = df[df["Type"].isin(type_choice)]
df = df[df["Background"].isin(background_choice)]
df = df[df["Base"].isin(base_choice)]
df = df[df["Outfit"].isin(outfit_choice)]
df = df[df["Necklace"].isin(necklace_choice)]
df = df[df["Eye"].isin(eye_choice)]
df = df[df["Beard"].isin(beard_choice)]
df = df[df["Hair"].isin(hair_choice)]
df = df[df["Hat"].isin(hat_choice)]
df = df[df["Hand_Accessories"].isin(hand_choice)]
df = df[df["Shoulder"].isin(shoulder_choice)]
df = df[df["Mouth"].isin(mouth_choice)]

traits = ['Background', 'Base', 'Outfit', 'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder', 'Mouth']

background_missing = [i for i in background if i not in pd.unique(df["Background"])]

with placeholder.container():
    st.image(df["image"].tolist(), caption=["# " + str(i) for i in df["number"]], width=100)  # Images

    st.markdown("### PP Details")
    st.dataframe(df[['number', 'Batch', 'Type', 'Total Score', 'Background', 'Base', 'Outfit', 'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder', 'Mouth',]])

    st.markdown("### Missing Traits")
    # st.dataframe(background_missing)
    st.write(background_missing)
    time.sleep(1)
