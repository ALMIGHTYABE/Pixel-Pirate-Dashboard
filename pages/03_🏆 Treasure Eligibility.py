# Importing Libraries
import time
import pandas as pd
import streamlit as st
import yaml

# App
st.set_page_config(
    page_title="Treasure",
    page_icon="icons/pp.png",
    layout="wide",
)

# Title
col1, col2 = st.columns(2)
col1.title("🏆 Treasure Eligibility")
col2.markdown('<div style="text-align: right;">Snapshot taken on 30th July</div>', unsafe_allow_html=True)

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Read Data
dataset_url = config["treasure"]["data"]


def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


df = get_data()

# Top-Level Filters
address_filter = st.selectbox("Select your address", pd.unique(df["address"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["address"] == address_filter]
df.reset_index(drop=True, inplace=True)

# Empty Placeholder Filled
with placeholder.container():
    if address_filter:
        if df["Treasures"][0] == 1:
            st.markdown("### You are eligible to receive {} treasure.".format(df["Treasures"][0]))

        else:
            st.markdown("### You are eligible to receive {} treasures.".format(df["Treasures"][0]))



    time.sleep(1)
