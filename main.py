import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  #  data web app development
import yaml

st.set_page_config(
    page_title="Pixel Pirate Tracker",
    page_icon="icons/pp.png",
    layout="wide",
)

params_path = "params.yaml"

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

config = read_params(params_path)

dataset_url = config["main"]["data-source"]

# Read Data
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()

# dashboard title
st.title("Pixel Pirate Dashboard")

# top-level filters
wallet_filter = st.selectbox("Select the Wallet", pd.unique(df["address"]))