# Importing Libraries
import requests
import time
import pandas as pd
import streamlit as st
import yaml
from st_btn_select import st_btn_select
import plotly.express as px

# App
st.set_page_config(
    page_title="Sales Tracker",
    page_icon="icons/pp.png",
    layout="wide",
)

# Title
st.title("🤑 Sales Tracker")
selection = st_btn_select(('Active Sales', 'Sales History'))

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
history_url = config["sales"]["history"]


def get_data(dataset) -> pd.DataFrame:
    return pd.read_csv(dataset)


nft_df = get_data(dataset_url)
sales_hist = get_data(history_url)  # History Data

# Scraping Data
r = requests.get(api_url)
sales = r.json()['sales']
sales_df = pd.json_normalize(sales)
sales_df['price'] = sales_df['price'].apply(lambda x: int(x) / 1000000000000000000)
sales_df['url'] = sales_df['id'].apply(
    lambda x: '<a href="https://paintswap.finance/marketplace/' + x + '">Sales Link</a>')
sales_df['tokenId'] = sales_df['tokenId'].apply(lambda x: int(x))
# sales_df = pd.merge(sales_df, nft_df[['number', 'name', 'image', 'Batch', 'Type', 'Total Score']], left_on='tokenId',
#                     right_on='number', how='left')
sales_df = pd.merge(sales_df, nft_df, left_on='tokenId', right_on='number', how='left')
sales_df['image'] = sales_df['image'].apply(lambda x: '<img src=' + x + ' width="100">')
sales_df['Rarity Score / FTM'] = sales_df['Total Score'] / sales_df['price']

if selection == "Active Sales":
    st.markdown("### Active Sales")

    # Sidebar Data
    batch = pd.unique(sales_df["Batch"])
    type = pd.unique(sales_df["Type"])
    background = pd.unique(sales_df["Background"])
    base = pd.unique(sales_df["Base"])
    outfit = pd.unique(sales_df["Outfit"])
    necklace = pd.unique(sales_df["Necklace"])
    eye = pd.unique(sales_df["Eye"])
    beard = pd.unique(sales_df["Beard"])
    hair = pd.unique(sales_df["Hair"])
    hat = pd.unique(sales_df["Hat"])
    hand = pd.unique(sales_df["Hand_Accessories"])
    shoulder = pd.unique(sales_df["Shoulder"])
    mouth = pd.unique(sales_df["Mouth"])

    # Sidebar - title & filters
    st.sidebar.markdown('### Data Filters')
    batch_choice = st.sidebar.multiselect(
    'Choose batch:', batch, default = batch)
    type_choice = st.sidebar.multiselect(
    'Choose type:', type, default = type)
    background_choice = st.sidebar.multiselect(
    'Choose background:', background, default = background)
    base_choice = st.sidebar.multiselect(
    'Choose base:', base, default = base)
    outfit_choice = st.sidebar.multiselect(
    'Choose outfit:', outfit, default = outfit)
    necklace_choice = st.sidebar.multiselect(
    'Choose necklace:', necklace, default = necklace)
    eye_choice = st.sidebar.multiselect(
    'Choose eye:', eye, default = eye)
    beard_choice = st.sidebar.multiselect(
    'Choose beard:', beard, default = beard)
    hair_choice = st.sidebar.multiselect(
    'Choose hair:', hair, default = hair)
    hat_choice = st.sidebar.multiselect(
    'Choose hat:', hat, default = hat)
    hand_choice = st.sidebar.multiselect(
    'Choose hand:', hand, default = hand)
    shoulder_choice = st.sidebar.multiselect(
    'Choose shoulder:', shoulder, default = shoulder)
    mouth_choice = st.sidebar.multiselect(
    'Choose mouth:', mouth, default = mouth)

    # dataframe filter
    sales_df = sales_df[sales_df["Batch"].isin(batch_choice)]
    sales_df = sales_df[sales_df["Type"].isin(type_choice)]
    sales_df = sales_df[sales_df["Background"].isin(background_choice)]
    sales_df = sales_df[sales_df["Base"].isin(base_choice)]
    sales_df = sales_df[sales_df["Outfit"].isin(outfit_choice)]
    sales_df = sales_df[sales_df["Necklace"].isin(necklace_choice)]
    sales_df = sales_df[sales_df["Eye"].isin(eye_choice)]
    sales_df = sales_df[sales_df["Beard"].isin(beard_choice)]
    sales_df = sales_df[sales_df["Hair"].isin(hair_choice)]
    sales_df = sales_df[sales_df["Hat"].isin(hat_choice)]
    sales_df = sales_df[sales_df["Hand_Accessories"].isin(hand_choice)]
    sales_df = sales_df[sales_df["Shoulder"].isin(shoulder_choice)]
    sales_df = sales_df[sales_df["Mouth"].isin(mouth_choice)]

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
        df.columns = ['Sales ID', 'PP Image', 'Name', 'Batch', 'Type', 'Rarity Score', 'Price in FTM',
                      'Rarity Score / FTM',
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
else:
    col1, col2 = st.columns(2)

    col1.markdown("### Sales History")
    col2.markdown('<div style="text-align: right;">Data is updated every 30 minutes</div>', unsafe_allow_html=True)

    # creating a single-element container
    placeholder = st.empty()

    # Empty Placeholder Filled
    with placeholder.container():
        sales_hist = sales_hist[
            ['id', 'image', 'nft.name', 'Batch', 'Type', 'Total Score', 'price', 'Rarity Score / FTM', 'endTime']]
        sales_hist.columns = ['Sales ID', 'PP Image', 'Name', 'Batch', 'Type', 'Rarity Score', 'Price in FTM',
                              'Rarity Score / FTM', 'Date Sold']

        fig = px.scatter(sales_hist, x='Date Sold', y='Price in FTM', color='Type', hover_name='Name',
                         hover_data=['Batch', 'Type', 'Rarity Score', 'Price in FTM', 'Rarity Score / FTM',
                                     'Date Sold'])
        fig.add_hline(y=47, line_width=2, line_dash='dot', line_color="green", annotation_text="Mint Price 47 FTM",
                      annotation_position="bottom right")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Last 100 Sales")
        sales_hist.sort_values(by=['Date Sold'], ascending=False, inplace=True)
        st.write(sales_hist.head(100).to_html(escape=False, index=False), unsafe_allow_html=True)
