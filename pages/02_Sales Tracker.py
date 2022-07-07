# Importing Libraries
import requests
import time
import pandas as pd
import streamlit as st
import yaml

# App
st.set_page_config(
    page_title="Sales Tracker",
    page_icon="icons/pp.png",
    layout="wide",
)

# Title
st.title("Sales Tracker")
st.markdown("### Active Sales")

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Read Data
dataset_url = config["main"]["data-source"]
api_url = config["sales"]["api"]


@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


nft_df = get_data()

# Scraping Data
r = requests.get(api_url)
sales = r.json()['sales']
sales_df = pd.json_normalize(sales)
sales_df['price'] = sales_df['price'].apply(lambda x: int(x) / 1000000000000000000)
sales_df['url'] = sales_df['id'].apply(
    lambda x: '<a href="https://paintswap.finance/marketplace/' + x + '">Sales Link</a>')
sales_df['tokenId'] = sales_df['tokenId'].apply(lambda x: int(x))
sales_df = pd.merge(sales_df, nft_df[['number', 'name', 'image', 'Batch', 'Type', 'Total Score']], left_on='tokenId',
                    right_on='number', how='left')
sales_df['image'] = sales_df['image'].apply(lambda x: '<img src=' + x + ' width="100">')
sales_df['Rarity Score / FTM'] = sales_df['Total Score'] / sales_df['price']

# Sorting
sort_option = st.selectbox(
    label="Sort by",
    options=('Price: Highest to Lowest', 'Price: Lowest to Highest', 'Rarity Score: Highest to Lowest',
             'Rarity Score: Lowest to Highest', 'Rarity Score / FTM: Highest to Lowest',
             'Rarity Score / FTM: Lowest to Highest'),
    index=0)

# creating a single-element container
placeholder = st.empty()

# Empty Placeholder Filled
with placeholder.container():
    df = sales_df[['id', 'image', 'name', 'Batch', 'Type', 'Total Score', 'price', 'Rarity Score / FTM', 'url']]
    df.columns = ['Sales ID', 'PP Image', 'Name', 'Batch', 'Type', 'Rarity Score', 'Price in FTM', 'Rarity Score / FTM',
                  'URL']

    if sort_option == 'Price: Highest to Lowest':
        df.sort_values(by=['Price in FTM'], ascending=False, inplace=True)
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    elif sort_option == 'Price: Lowest to Highest':
        df.sort_values(by=['Price in FTM'], ascending=True, inplace=True)
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    elif sort_option == 'Rarity Score: Highest to Lowest':
        df.sort_values(by=['Rarity Score'], ascending=False, inplace=True)
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    elif sort_option == 'Rarity Score: Lowest to Highest':
        df.sort_values(by=['Rarity Score'], ascending=True, inplace=True)
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    elif sort_option == 'Rarity Score / FTM: Highest to Lowest':
        df.sort_values(by=['Rarity Score / FTM'], ascending=False, inplace=True)
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        df.sort_values(by=['Rarity Score / FTM'], ascending=True, inplace=True)
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    time.sleep(1)
