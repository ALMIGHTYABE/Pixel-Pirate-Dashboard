import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # data web app development
import yaml
from PIL import Image

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
st.title("Pixel Pirate Tracker")

# top-level filters
address_filter = st.multiselect("Select your address", pd.unique(df["address"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df.address.isin(address_filter)]

st.image(df["image"].tolist(), width=100)


st.markdown("### Detailed Data View")
st.dataframe(df)



