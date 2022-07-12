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
st.title("🏆 Treasure Eligibility")

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Read Data
dataset_url = config["main"]["data-source"]


# @st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


df = get_data()

# Top-Level Filters
address_filter = st.selectbox("Select your address", pd.unique(df["address"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["address"] == address_filter]

# Computing Eligibility
batch_counts = pd.DataFrame(df['Batch'].value_counts())
batch_counts.reset_index(inplace=True)
batch_counts.columns = ['Batch', 'Number of PPs']
batch_counts.sort_values(by=['Batch'], axis=0, inplace=True)
batch_counts.style.hide(axis="index")
min_pp = batch_counts['Number of PPs'].min()
batch_counts['Bool'] = batch_counts['Number of PPs'].apply(lambda i: True if i >= min_pp else False)

# Empty Placeholder Filled
with placeholder.container():
    if address_filter:
        if (batch_counts['Bool'].all(axis=0)) & (min_pp == 1) & (len(batch_counts) == 6):
            st.markdown("### You are eligible to receive {} treasure.".format(min_pp))
            st.write(batch_counts[['Batch', 'Number of PPs']].to_html(escape=False, index=False),
                     unsafe_allow_html=True)
        elif (batch_counts['Bool'].all(axis=0)) & (min_pp > 1) & (len(batch_counts) == 6):
            st.markdown("### You are eligible to receive {} treasures.".format(min_pp))
            st.write(batch_counts[['Batch', 'Number of PPs']].to_html(escape=False, index=False),
                     unsafe_allow_html=True)
        else:
            st.markdown(
                "### You are not eligible to receive any treasures. Collect one Pixel Pirate from each batch to be eligible.")
            st.write(batch_counts[['Batch', 'Number of PPs']].to_html(escape=False, index=False),
                     unsafe_allow_html=True)
    time.sleep(1)
